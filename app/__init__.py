# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_wtf.csrf import CSRFProtect

from config import config
from app.library.assets import app_css, app_js, vendor_css, vendor_js

# 全局变量
basedir = os.path.abspath(os.path.dirname(__file__))
mail = Mail()
db = MongoEngine()
csrf = CSRFProtect()
compress = Compress()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

def create_app(config_name):
    '''
    创建APP
    :param config_name:
    :return:
    '''
    app = Flask(
        __name__,
        template_folder=config[config_name].TEMPLATE_FOLDER,
        static_folder=config[config_name].STATIC_FOLDER,
        static_url_path=config[config_name].STATIC_URL_PATH
    )
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Set up extensions
    cors_options = {"supports_credentials": True}
    cors = CORS(app, **cors_options)
    api = Api(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # import routers
    from app.routers.main import main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routers.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.routers import account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from app.routers import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from app.routers import todo_blueprint
    app.register_blueprint(todo_blueprint, url_prefix='/todo')

    return app
