# -*- coding: utf-8 -*-

import os, sys
from app.library.config.parser import Parser


config_file = './conf/dev.conf'
parser = Parser()
parser.load(config_file)

class DevelopmentConfig(parser._config):
    DEBUG = True
    ASSETS_DEBUG = True
    MONGO_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or None

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(parser._config):
    TESTING = True
    MONGO_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or None
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(parser._config):
    MONGO_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or None
    SSL_DISABLE = (os.environ.get('SSL_DISABLE') or 'True') == 'True'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


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
