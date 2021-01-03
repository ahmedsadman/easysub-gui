# EasySub

## Download movie subtitles with ease

Easysub is a program written in wxPython that automatically downloads movie subtitles based on file hash. It uses the OpenSubtitles API to search and download subtitles.

![Screenshot](https://i.imgur.com/O4djmgX.png)

### Features

-   Drag and drop multiple files to download subtitles
-   Subtitles are renamed and copied to the directory which makes multimedia players easily find the corresponding SRT file

### Usage

You need to have the following to run this program:

-   Python 3.6.x
-   An account in [OpenSubtitles](https://www.opensubtitles.org) with registered API agent

Now do the steps as follows:

-   Create a virtual environment and install the requirements using `pip install -r requirements.txt`
-   Create a `.env` file in the root directory supplying `agent` info provided by OpenSubtitles API
-   Start the program using `python main.py`
-   (Optional) Upon starting, please provide your OpenSub creds in `Menu > Account info`.

You can ignore putting account info, in that case guest login will be used (not recommended).

### Binary Distribution

A standalone binary distribution is available for Windows. Please look into the _Releases_ tab to download the latest version. Just download it, unzip and click _EasySub.exe_, it's out of the box and ready to use. Windows distribution will be maintained regularly

For generating builds _pyinstaller_ is used. If you need to generate builds for other OS, clone this repo and follow documentation of _pyinstaller_ as required.
