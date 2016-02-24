try:
    import ujson as json
except ImportError:
    import json
import os
import logging

from os.path import expanduser
home = expanduser("~")

PATH_CONFIG_JSON = "./config.json"

class GlobalConfig:
    """
    Config class providing configuration parameters, and a way to persist those parameters 
    or load them from a file
    """
    class MongoDB:
        def __init__(self):
            self.name = "test_monitoring"
            self.host = "0.0.0.0"
            self.port = 27017

        @classmethod
        def from_config(cls, dict_config):
            """
            load the class with given values
            :param dict_config: dict of the corresponding key, values
            :return: an object loaded with the given values.
            """
            mongo_db = cls()
            mongo_db.name = dict_config['name']
            mongo_db.host = dict_config['host']
            mongo_db.port = dict_config['port']
            return mongo_db

        def save_config(self):
            dict_config= {}
            dict_config['name'] = self.name 
            dict_config['host'] = self.host 
            dict_config['port'] = self.port 
            return dict_config


    class WebServer:
        def __init__(self):
            self.host = "0.0.0.0"
            self.port = 8080

        @classmethod
        def from_config(cls, dict_config):
            web_server = cls()
            web_server.host = dict_config['host']
            web_server.port = dict_config['port']
            return web_server

        def save_config(self):
            dict_config= {}
            dict_config['host'] = self.host 
            dict_config['port'] = self.port 
            return dict_config

    def __init__(self, path_config):
        """ Construct with the development configuration """

        self.mongo_db = GlobalConfig.MongoDB()
        self.database_log = True
        self.web_server = GlobalConfig.WebServer()
        self.path_log = "./log/"
        self.logger_level = logging.DEBUG
        self.path_config = path_config

    def from_config(self):
        dict_config = {}
        with open(self.path_config, 'r') as infile:
            dict_config = json.loads(infile.read())
        #global_config = cls()
        self.mongo_db = GlobalConfig.MongoDB.from_config(dict_config['mongo_db'])
        self.database_log = dict_config['database_log']
        self.web_server = GlobalConfig.WebServer.from_config(dict_config['web_server'])
        self.path_log = dict_config['path_log']
        self.logger_level = dict_config['logger_level']

        #return global_config

    def save_config(self):
        dict_config= {}
        dict_config['mongo_db'] = self.mongo_db.save_config()    
        dict_config['web_server'] = self.web_server.save_config()          
        dict_config['path_log'] = self.path_log
        dict_config['str_to_replace_id'] = self.str_to_replace_id
        dict_config['logger_level'] = self.logger_level
        with open(self.path_config, 'w') as outfile:
            outfile.write(json.dumps(dict_config))

CONFIG = None

def init_config(config_file_path):
    config = GlobalConfig(config_file_path)
    config.from_config()

    globals()['CONFIG'] = config
if __name__ == '__main__':
    gc = GlobalConfig("./config.json").save_config()