import configparser

class Configs:
    def __init__(self, param = 'DATA_APP_CONFIGS'):
        self.param = param

    def get_data_config(self, param='DATA_APP_CONFIGS'):
        """
        Reads config file and gets data as a key,value pair dictionary
        """
        conf = {}
        cfg = configparser.ConfigParser()
        cfg.read('data.conf')
        for (key,val) in cfg.items(param):
            conf[key]=val
        self.conf = conf
        return conf