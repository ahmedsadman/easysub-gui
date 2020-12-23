from xmlrpc.client import ServerProxy
import os
import urllib.request as urllib, gzip, sys
from .hash import calculate_hash
from .static import Static


# the main class to download subtitles using api
class SubtitleHandler:
    def __init__(self, auth, language="None"):
        self.auth = auth
        self.rpc = self.auth.get_rpc()

    def get_hash(self, path):
        return calculate_hash(path)

    def process_sub(self, Format, path):
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
        self.cleanup()
        print("complete")

    def cleanup(self):
        os.remove("sub.gz")

    def search(self, path):
        # api processing
        self.hash = self.get_hash(path)
        token = self.auth.get_token()
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
        self.download_sub(path)
        return True

    def download_sub(self, path):
        print("Downloading Subtitle...")
        opener = urllib.URLopener()
        opener.retrieve(self.Download, "sub.gz")
        print("\nFile Downloaded")
        Val = self.process_sub(self.subFormat, path)  # True or False
