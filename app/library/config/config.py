# -*- coding: utf-8 -*-

class Config:
    '''
    default config
    '''
    DEBUG=False,
    TESTING=False,
    BCRYPT_LEVEL=13,
    APP_NAME='Flask-Mongo',
    SECRET_KEY="__SECRET_KEY__",
    WTF_CSRF_ENABLED=True,
    TEMPLATE_FOLDER="%(PROJECT_PATH)s/template",
    STATIC_FOLDER="%(PROJECT_PATH)s/static",
    STATIC_URL_PATH="/static",

    @staticmethod
    def init_app(app):
        pass

    def instance(self):
        return Config()