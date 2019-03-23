from flask import Blueprint, render_template
import redis, gevent

ws = Blueprint('ws', __name__, url_prefix='/ws')

# 这个 Redis 客户端用来接收前端发来的数据并将数据处理后发送到指定频道
# 并将频道中的消息接收出来发送给订阅频道的用户
# 为什么要把数据从 Redis 的发布订阅系统过一遍呢？
# 因为这样可以保证消息是顺序收发的
r = redis.from_url('redis://127.0.0.1:6379')

class Chatroom:
    def __init__(self):
        self.clients = []  # 用户列表
        self.pubsub = r.pubsub()  # 利用 Redis 客户端创建发布订阅系统
        self.pubsub.subscribe('科教频道')  # 订阅科教频道

    # 注册用户，也就是把订阅科教频道的用户放在一个列表里
    def register(self, chat):
        self.clients.append(chat)

    # 36 行会用到这个方法，把消息发送给用户
    def send(self, client, data):
        try:
            client.send(data.decode('utf-8'))
        except:
            self.clients.remove(client)

    def run(self):
        # 发布订阅系统监听科教频道中的消息
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message['data'].decode()
                # 收到消息后发送给订阅科教频道的用户
                for client in self.clients:
                    gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)

# 创建聊天室，启动发布订阅系统的监听频道的功能
chat = Chatroom()
chat.start()

# 使用 flask-sockets 后，ws 链接对象会被自动注入到路由处理函数
# 该处理函数用来处理前端发过来的数据并向订阅频道发送消息
# 其实 ws 是就是用户啦，前端数据是它传来的，订阅频道的用户也是它们
# 这个视图函数里的 ws 是发消息的用户
@ws.route('/send')
def inbox(ws):
    # 循环里面的 receive 函数是在阻塞运行的，直到前端发送数据过来
    # 收到数据后将其发布到科教频道，也就是我们的消息队列中
    # 这样一直循环，直到 websocket 连接关闭
    while not ws.closed:
        message = ws.receive()
        if message:
            r.publish('科教频道', message)

# 这里的 ws 是接收消息的用户，也就是在聊天室里的，当然发消息的用户也会收到消息
@ws.route('/receive')
def outbox(ws):
    chat.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)
