from xmlrpc.client import ServerProxy
import hashCheck, os
import urllib.request as urllib, gzip, sys

server = "http://api.opensubtitles.org/xml-rpc"

# this class processess all things related to subtitle and movie files
class FileProcessor(object):
    def LoginData(self):
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

    def GetHash(self, path):
        return hashCheck.hash(path)

    def ProcessSub(self, Format, path):
        # unpacks subtitle file, places it in the movie folder, and renames it according to the movie name
        print("Unpacking subtitle file...\n")
        Path = path
        movieFile = os.path.basename(Path)
        subFileName = os.path.splitext(Path)[0] + "." + Format

        with gzip.open("sub.gz", "rb") as comp:
            content = comp.read()
            with open(subFileName, "wb") as f:
                f.write(content)
            if not f.closed:
                f.close()
        if not comp.closed:
            comp.close()
        self.CleanUp()
        print("complete")

    def CleanUp(self):
        os.remove("sub.gz")


# the main class to download subtitles using api
class MainEngine(object):
    def __init__(self, language="None"):
        self.rpc = ServerProxy(
            server, allow_none=True
        )  # allow_none is mandatory to make some methods work
        self.user_agent = "muhib96"  # my registered user agent for opensub api
        self.File = (
            FileProcessor()
        )  # a variable needed to access the FileProcessor class

    def getToken(self):
        # function to login the user
        print("Inside gettoken func")
        try:
            return self.Token
        except AttributeError:
            print("Logging in...")
            data = self.File.LoginData()
            User = data[0]
            Pass = data[1]
            self.logindata = self.rpc.LogIn(User, Pass, "eng", self.user_agent)
            if "200 OK" not in self.logindata["status"]:
                return False
            # print self.logindata
            self.Token = self.logindata["token"]
            print("login complete")
            return self.Token

    def logout(self, token):
        # function to logout
        self.rpc.LogOut(token)
        print("Logout success")

    def subSearch(self, path):
        # api processing
        self.hash = self.File.GetHash(path)
        token = self.getToken()
        print("Please wait...")
        self.param = [
            token,  # token
            {
                "sublanguageid": "eng",  # sublanguageid
                "moviehash": self.hash,  # hash
                "moviesize": os.path.getsize(path),  # byte size
            },
        ]
        Obj = self.rpc.SearchSubtitles(token, self.param)
        if not Obj["data"]:
            print("Subtitle not found for this file...")
            return False

        # gets the data related to downloaing the subtitle
        self.Download = Obj["data"][0]["SubDownloadLink"]
        self.subFormat = Obj["data"][0]["SubFormat"]

        # subtitle download
        self.DownloadSub(path)
        return True

    def DownloadSub(self, path):
        print("Downloading Subtitle...")
        opener = urllib.URLopener()
        opener.retrieve(self.Download, "sub.gz")
        print("\nFile Downloaded")
        Val = self.File.ProcessSub(self.subFormat, path)  # True or False
