# -*- coding: utf-8 -*-

import logging
import traceback
import ast
from configparser import ConfigParser
from .config import Config

configParser = ConfigParser()

class Parser(object):

    _config = Config()

    def load(self, config_file=None):
        '''
        load config data from config file
        :param config_file:
        :return:
        '''
        if not config_file:
            raise Exception('10100', 'Error config file')

        configParser.read(config_file, encoding='UTF-8')
        self.assemble()

    def get_config(self):
        '''
        get config
        :return:
        '''
        return self._config

    def parse(self, section, options):
        '''
        parse config
        :param section:
        :param options:
        :return:
        '''
        for option in options:
            config = configParser.get(section, option)
            try:
                config = ast.literal_eval(config)
            except Exception as e:
                logging.error(traceback.format_exc())

            self._config.__setattr__(option, config)


    def assemble(self):
        '''
        assemble config
        :return:
        '''
        if configParser.sections():
            for section in configParser.sections():
                options = configParser.options(section)
                if section == 'APP':
                    self.parse(section, options)
                else:
                    if 'enabled' in options:
                        enabled = ast.literal_eval(configParser.get(section, 'enabled'))
                        if enabled:
                            options.remove('enabled')
                            self.parse(section, options)
                        else:
                            continue
