# -*- coding: utf-8 -*-

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
    TEMPLATE_FOLDER="%(PROJECT_PATH)s/template"
    STATIC_FOLDER="%(PROJECT_PATH)s/static"
    STATIC_URL_PATH="/static"

    MAIL_SETTINGS = {
        'MAIL_SERVER': 'smtpdm.aliyun.com',
        'MAIL_PORT': 465,
        'MAIL_USE_TLS': True,
        'MAIL_USE_SSL': False,
        'MAIL_USERNAME': '',
        'MAIL_PASSWORD': '',
        'MAIL_DEFAULT_SENDER': '',
    }

    REDIS_URL='redis://:password@localhost/0'

    MYSQL_SLOW_DB_QUERY_TIME=0.5
    SQLALCHEMY_BINDS = dict(
        base='mysql+pymysql://work:work@localhost:3306/base',
        account='mysql+pymysql://work:work@localhost:3306/account',
    )

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

    @staticmethod
    def init_app(app):
        pass

