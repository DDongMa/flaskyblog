# -*- coding:utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from .exceptions import db
from config import config
from .exceptions import login_manager
from flask_pagedown import PageDown
from flask_admin import Admin
from .admin import CustomView, CustomModelView
from .models import User, Post, Comment

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()


pagedown = PageDown()
admin = Admin(name=u'后台管理系统')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    db.init_app(app)

    login_manager.init_app(app)
    pagedown.init_app(app)

    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))
    admin.add_view(CustomModelView(User, db.session, category=u'用户'))
    admin.add_view(CustomModelView(Post, db.session, category=u'用户'))
    admin.add_view(CustomModelView(Comment, db.session, category=u'用户'))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
