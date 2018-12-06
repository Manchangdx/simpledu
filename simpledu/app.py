from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sockets import Sockets
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from .config import configs
from .models import db, User, Course

def register_blueprints(app):
    from .handlers import front, admin, course, live, ws
    for i in (admin, front, course, live, ws):
        app.register_blueprint(i)
    sockets = Sockets(app)
    sockets.register_blueprint(ws)

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    l = LoginManager()
    l.init_app(app)

    @l.user_loader
    def user_loader(id):
        return User.query.get(id)

    l.login_view = 'front.login'

def create_app(c):
    app = Flask(__name__)
    app.config.from_object(configs.get(c))
    register_blueprints(app)
    register_extensions(app)
    return app
