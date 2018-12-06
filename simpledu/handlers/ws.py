from flask import Blueprint, render_template
import redis, gevent

ws = Blueprint('ws', __name__, url_prefix='/ws')

r = redis.from_url('redis://127.0.0.1:6379')

class Chatroom:
    def __init__(self):
        self.clients = []  # 客户端列表
        self.pubsub = r.pubsub()  # 创建发布订阅系统
        self.pubsub.subscribe('科教频道')  # 订阅科教频道

    # 注册客户端
    def register(self, chat):
        self.clients.append(chat)

    def send(self, client, data):
        try:
            client.send(data.decode('utf-8'))
        except:
            self.clients.remove(client)

    def run(self):
        # 用 redis 客户端监听消息
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message['data']
                for client in self.clients:
                    gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)

chat = Chatroom()
chat.start()

@ws.route('/send')
def inbox(ws):
    while not ws.closed:
        message = ws.receive()
        if message:
            r.publish('科教频道', message)

@ws.route('/receive')
def outbox(ws):
    chat.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)
