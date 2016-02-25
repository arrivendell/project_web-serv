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
            self.name = "webserver_db"
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
            self.logger_name = "webito"
            self.nbr_ts_returned = 5
            self.max_size_list_ts = 6
            self.path_key_server = "tls/serverkey.key"
            self.path_cert_server = "tls/servercert.cert"
            self.is_https = False

        @classmethod
        def from_config(cls, dict_config):
            web_server = cls()
            web_server.host = dict_config['host']
            web_server.port = dict_config['port']
            web_server.logger_name = dict_config['logger_name']
            web_server.nbr_ts_returned = dict_config['nbr_ts_returned']
            web_server.max_size_list_ts = dict_config['max_size_list_ts']
            web_server.path_key_server = dict_config['path_key_server']
            web_server.path_cert_server = dict_config['path_cert_server']
            web_server.is_https = dict_config['is_https']
            return web_server

        def save_config(self):
            dict_config= {}
            dict_config['host'] = self.host 
            dict_config['port'] = self.port 
            dict_config['logger_name'] = self.logger_name 
            dict_config['nbr_ts_returned'] = self.nbr_ts_returned 
            dict_config['max_size_list_ts'] = self.max_size_list_ts 
            dict_config['path_key_server'] = self.path_key_server 
            dict_config['path_cert_server'] = self.path_cert_server 
            dict_config['is_https'] = self.is_https 
            return dict_config

    def __init__(self, path_config):
        """ Construct with the development configuration """

        self.mongo_db = GlobalConfig.MongoDB()
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
        self.web_server = GlobalConfig.WebServer.from_config(dict_config['web_server'])
        self.path_log = dict_config['path_log']
        self.logger_level = dict_config['logger_level']

        #return global_config

    def save_config(self):
        dict_config= {}
        dict_config['mongo_db'] = self.mongo_db.save_config()    
        dict_config['web_server'] = self.web_server.save_config()          
        dict_config['path_log'] = self.path_log
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