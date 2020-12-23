import os
from dotenv import load_dotenv

load_dotenv()


class Static:
    server_url = "http://api.opensubtitles.org/xml-rpc"
    agent = os.environ.get("agent")
    datafile = "Account.bin"
