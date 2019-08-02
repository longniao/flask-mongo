# -*- coding: utf-8 -*-

import os
import urllib.parse

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    '''
    default config
    '''
    DEBUG=False
    TESTING=False
    BCRYPT_LEVEL=13
    APP_NAME='Flask-Mongo'
    SECRET_KEY="__SECRET_KEY__"
    WTF_CSRF_ENABLED=True
    TEMPLATE_FOLDER="%s/website/templates" % basedir
    STATIC_FOLDER="%s/website/assets" % basedir
    STATIC_URL_PATH="/static"

    # Mail settings
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'noreply@example.com'
    MAIL_PASSWORD = ''
    MAIL_SUBJECT_PREFIX = '[Flasky Mongo]'
    MAIL_SENDER = 'Flasky Mongo <noreply@example.com>'

    # Admin account
    ADMIN_PASSWORD = 'password'
    ADMIN_EMAIL = 'flask-mongo@example.com'

    #REDIS_URL = 'redis://username:password@localhost:27017/0'
    REDIS_URL = 'redis://localhost:6379/0'

    # Parse the REDIS_URL to set RQ_REDIS_URL
    RQ_REDIS_URL = REDIS_URL

    # Mysql
    MYSQL_SLOW_DB_QUERY_TIME=0.5
    SQLALCHEMY_BINDS = dict(
        base='mysql+pymysql://work:work@localhost:3306/base',
        account='mysql+pymysql://work:work@localhost:3306/account',
    )

    # Mongodb
    MONGODB_SETTINGS = [{
        'ALIAS': 'base',
        'HOST': 'localhost',
        'PORT': 27017,
        'DB': 'flask_mongo',
        'USERNAME': None,
        'PASSWORD': None,
    }, {
        'ALIAS': 'account',
        'HOST': 'localhost',
        'PORT': 27017,
        'DB': 'flask_mongo',
        'USERNAME': None,
        'PASSWORD': None,
    }]

    # Language
    LANGUAGES = {
        'en': 'English',
        'es': 'Español',
        'cn': "Chinese",
    }

    @staticmethod
    def init_app(app):
        pass

