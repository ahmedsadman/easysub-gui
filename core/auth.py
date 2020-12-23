from xmlrpc.client import ServerProxy
from .static import Static


class Auth:
    def __init__(self):
        self.rpc = ServerProxy(
            Static.server_url, allow_none=True
        )  # allow_none is mandatory to make some methods work
        self.Token = None
        self.user_agent = Static.agent

    def get_rpc(self):
        return self.rpc

    def get_user_agent(self):
        return self.user_agent

    def get_login_data(self):
        # to access the OpenSub api, every user should have an account,
        # the account credentials are stored in the folder Login.txt,
        # this function retrieves the data from the said file
        with open("Login.txt", "r") as f:
            x = f.readlines()
            x1 = x[0].strip()  # strip function is used to avoid Newlines
            x2 = x[1].strip()
            LoginInfo = (
                x1[x1.index("=") + 1 :],
                x2[x2.index("=") + 1 :],
            )  # only selects the texts which are after the equal sign, check Login.txt
            if LoginInfo[0] == "" or LoginInfo[1] == "":
                LoginInfo = (
                    None,
                    None,
                )  # Anonymous login is supported, it executes if no Logindata is provided
                # print a warning message if logindata not found, because it may result Status Code 401 Unauthorized
                print(
                    "WARNING: This program requires your userinfo to work properly. Please provide your login credentials in Login.txt\nTrying anonymous login\n"
                )
        if not f.closed:
            f.close()
        return LoginInfo

    def login(self):
        print("Logging in...")
        data = self.get_login_data()
        User = data[0]
        Pass = data[1]
        self.logindata = self.rpc.LogIn(User, Pass, "eng", self.user_agent)
        if "200 OK" not in self.logindata["status"]:
            return False

        self.Token = self.logindata["token"]
        print("login complete")
        return self.Token

    def get_token(self):
        # function to login the user
        if self.Token is None:
            return self.login()
        return self.Token

    def logout(self):
        # function to logout
        self.rpc.LogOut(self.Token)
        print("Logout success")