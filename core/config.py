import pickle
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    IMPORTANT: This requires .ENV file to create the "config.bin" for the
    first time. So after creating binary distribution, initially a .ENV file should be provided
    with required data. When the config.bin is created, the .ENV must be deleted (for security)
    and the binary can be distributed as usual (along with the config.bin of course)
    """

    __instance__ = None
    filename = "config.bin"

    def __init__(self):
        # singleton
        if Config.__instance__ is None:
            self.server_url = "http://api.opensubtitles.org/xml-rpc"
            self.user_agent = os.environ.get("agent")
            self.username = None
            self.password = None
            Config.__instance__ = self
        else:
            raise Exception("You cannot create multiple instance of Config class")

    @staticmethod
    def get_instance():
        if Config.__instance__ is None:
            instance = None
            if Config.exists():
                # if config file found, load it
                print("-- Load Config --")
                instance = Config.load()
            else:
                # create the config file
                print("-- Create Config --")
                instance = Config()
                Config.save(instance)
            Config.__instance__ = instance
        return Config.__instance__

    @staticmethod
    def exists():
        return os.path.exists(Config.filename)

    @staticmethod
    def load():
        with open(Config.filename, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def save(cls):
        with open(Config.filename, "wb") as f:
            pickle.dump(cls, f)

    def get(self, key):
        return getattr(self, key)

    def set(self, key, value):
        setattr(self, key, value)
        Config.save(self)