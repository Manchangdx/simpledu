import redis
import gevent
from flask import Blueprint


ws = Blueprint('ws', __name__, url_prefix='/ws')

# 此对象是一个 Redis 客户端，它既可以发布消息到频道，也可以订阅频道
redis = redis.from_url('redis://127.0.0.1:6379')


class Chatroom:

    def __init__(self):
        self.clients = []               # 用户列表
        self.pubsub = redis.pubsub()    # 初始化发布订阅系统
        self.pubsub.subscribe('chat')   # 订阅 chat 频道

    def register(self, client):
        """注册用户，把用户添加到用户列表里
        
        :para client: geventwebsocket.websocket.WebSocket 类的实例
        """
        self.clients.append(client)

    def send(self, client, data):
        """发送数据给浏览器

        :para client: geventwebsocket.websocket.WebSocket 类的实例
        :para data: 要发送的消息，二进制字典字符串 b'{"user": xxx}'
        """
        # 调用 client 的 send 方法给浏览器发送消息
        # 如果出现异常，表示连接已关闭，将客户端移除
        try:
            client.send(data.decode())
        except:
            self.clients.remove(client)

    def run(self):
        # 下面一行代码中发布订阅系统对象 self.pubsub 的 listen 方法处于阻塞状态
        # 这里之所以使用 Redis 的发布订阅系统
        # 就是因为它能阻塞监听，并且消息队列功能保证消息按照先进先出的次序移动
        # 当用户在浏览器页面输入信息并点击「发言」按钮后
        # 浏览器调用 inbox 对象向服务器发送数据
        # 服务器的视图函数调用 geventwebsocket.websocket.WebSocket 类的
        # 实例的 receive 方法接收数据
        # 然后 redis 客户端调用 publish 方法向 chat 频道发送此数据
        # 此处收到消息，进入 for 循环
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                # 要发送给浏览器的数据，二进制字典字符串 b'{"user": xxx}'
                data = message.get('data')
                # 向用户列表中的全部用户发送数据
                # 也就是 geventwebsocket.websocket.WebSocket 实例向浏览器发送数据
                for client in self.clients:
                    # 发送消息需要一小段时间，这里使用 gevent 异步发送
                    gevent.spawn(self.send, client, data)

    def start(self):
        # 因为 self.run 方法会阻塞运行，这里使用异步执行
        gevent.spawn(self.run)


chat = Chatroom()   # 初始化聊天室对象，也就是 redis 订阅 chat 频道
chat.start()        # 异步启动 redis 的 PUB/SUB 系统的「监听已订阅频道」功能


# 当浏览器发送 '/live' 路由的请求到服务器，服务器返回响应对象
# 然后浏览器会创建一个遵守 WebSocket 协议的对象 inbox 
# 并向服务器发送一个请求，请求的路由是该对象的 url 属性值，也就是 '/ws/send'
# 服务器收到请求后根据请求信息创建一个 environ 字典对象
# 该字典对象的 'wsgi.websocket' 键对应的值
# 就是 geventwebsocket.websocket 模块中的 WebSocket 类的实例
# 下面这个视图函数的参数 ws 就是该实例，它就是一个 WebSocket 服务器
@ws.route('/send')
def inbox(ws):
    # 注册用户，也就是把 ws 放到聊天室的 clients 列表里
    chat.register(ws)
    while not ws.closed:
        # 这里 receive 方法阻塞运行
        # 等待前端的 inbox 对象执行 send 方法发送信息过来
        message = ws.receive()
        if message:
            # redis 就是一个 Redis 客户端
            # 把消息发送到 chat 频道，订阅此频道的客户端就会收到消息
            redis.publish('chat', message)
