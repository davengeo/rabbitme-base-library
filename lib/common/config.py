import configparser
import os


class Config(object):

    def __init__(self, path_file: str):
        self.path_file = path_file
        self.config = configparser.ConfigParser()
        self.config.read(path_file)

    def get_value(self, section: str, key: str) -> str:
        return self.config[section][key]

    def get_path(self, key: str) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(self.path_file), self.config['Paths'][key]))
