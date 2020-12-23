from xmlrpc.client import ServerProxy
import os
import urllib.request as urllib, gzip, sys
from .hash import calculate_hash

server = "http://api.opensubtitles.org/xml-rpc"


# the main class to download subtitles using api
class SubtitleHandler:
    def __init__(self, auth, language="None"):
        self.auth = auth
        self.rpc = self.auth.get_rpc()

    def GetHash(self, path):
        return calculate_hash(path)

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

    def subSearch(self, path):
        # api processing
        self.hash = self.GetHash(path)
        token = self.auth.getToken()
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
        Val = self.ProcessSub(self.subFormat, path)  # True or False
