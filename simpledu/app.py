from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sockets import Sockets

from simpledu.configs import configs
from simpledu.models import db, Course, User
from simpledu.handlers import bp_list, ws


def register_blueprints(app):
    """注册蓝图
    """

    for bp in bp_list:
        app.register_blueprint(bp)

    # 将应用对象作为参数创建套接字对象
    # 这里会调用套接字对象的 init_app 方法将应用对象的核心方法 wsgi_app
    # 替换成 SocketMiddleware 类的实例，该类也定义在 flask_sockets 模块中
    # 当客户端的请求进来之后，会调用应用对象的 wsgi_app 方法
    # 其实就是调用 SocketMiddleware 实例的 __call__ 方法
    sockets = Sockets(app)
    # 注册蓝图，此方法会调用蓝图对象自身的 register 方法
    # 通常情况下，调用蓝图自身的 register 方法时 app 参数值是应用对象
    # 但这里的 register_blueprint 方法会将套接字对象作为 app 参数值
    # 也就是蓝图中的视图函数会在套接字对象中备案
    sockets.register_blueprint(ws)


def register_extensions(app):
    """注册扩展
    """

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'
    login_manager.login_message = '需要先登录，然后才能访问此页面。'
    login_manager.login_message_category = 'warning'


def create_app(config):
    """此函数为工厂函数，用于创建应用对象并返回
    """

    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    register_blueprints(app)
    register_extensions(app)

    return app
