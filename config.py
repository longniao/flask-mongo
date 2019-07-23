# -*- coding: utf-8 -*-

import os, sys
from app.library.config.parser import Parser
from conf.dev import Config

'''
config_file = './conf/dev.conf'
parser = Parser()
parser.load(config_file)
'''

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    SSL_DISABLE = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert Config.SECRET_KEY, 'SECRET_KEY IS NOT SET!'


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig
}
config_env = 'production'