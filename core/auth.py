import os
from xmlrpc.client import ServerProxy
from .config import Config


class Auth:
    def __init__(self):
        self.config = Config.get_instance()
        self.rpc = ServerProxy(
            self.config.get("server_url"), allow_none=True
        )  # allow_none is mandatory to make some methods work
        self.Token = None
        self.user_agent = self.config.get("user_agent")

    def get_rpc(self):
        return self.rpc

    def get_user_agent(self):
        return self.user_agent

    def login(self):
        User = self.config.get("username")
        Pass = self.config.get("password")
        self.logindata = self.rpc.LogIn(User, Pass, "eng", self.user_agent)
        if "200 OK" not in self.logindata["status"]:
            return False

        self.Token = self.logindata["token"]
        return self.Token

    def get_token(self):
        # function to login the user
        if self.Token is None:
            return self.login()
        return self.Token

    def logout(self):
        # function to logout
        self.rpc.LogOut(self.Token)