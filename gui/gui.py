import wx
import sys
import time
from core import SubtitleHandler, Auth
from threading import Thread
from wx.adv import AboutBox
from wx.adv import AboutDialogInfo
from wx.lib.wordwrap import wordwrap
from .change_account import ChangeAccountGUI
from .filedrop import FileDrop
from .list import AutoWidthListCtrl


class GUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        # wx.Frame.__init__(self, parent, id, title, size=(380, 230))
        super(GUI, self).__init__(*args, **kwargs)
        self.font = wx.Font(
            pointSize=10, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD
        )
        self.auth = Auth()
        self.login_user()
        self.sub_handler = SubtitleHandler(self.auth)

    def login_user(self):
        try:
            wait = wx.BusyInfo("Logging in, please wait...")
            self.token = self.auth.get_token()  # login the user
        except Exception as e:
            print(e)
            del wait
            wx.MessageBox(
                "Login failed. Please check internet connection",
                "Login Error",
                wx.OK | wx.ICON_ERROR,
            )
            sys.exit(-1)
        del wait

        if not self.token:
            print("login error")
            wx.MessageBox(
                "Cannot login with the provided username/pass combination.\nPlease type in your account info in the next window",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )
            dlg = ChangeAccountGUI(None, -1, "Account Info")
            dlg.ShowModal()
            try:
                dlg.Destroy()
            except:
                pass
            self.Destroy()

        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)
        ID_ABOUTBOX = wx.NewIdRef()
        ID_CHANGEACMENU = wx.NewIdRef()

        # menu bar
        menubar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(ID_CHANGEACMENU, "Account info")
        menu.Append(ID_ABOUTBOX, "About")

        menubar.Append(menu, "&Menu")
        self.SetMenuBar(menubar)

        self.st1 = wx.StaticText(panel, label="Drag && Drop movie files below")
        self.st1.SetFont(self.font)

        self.btnDownlaod = wx.Button(panel, label="Download", size=(90, 40))
        self.btnReset = wx.Button(panel, label="Reset", size=(90, 40))
        self.btnQuit = wx.Button(panel, label="Quit", size=(90, 40))

        self.list = AutoWidthListCtrl(panel)
        self.list.InsertColumn(0, "File", width=420)
        self.list.InsertColumn(1, "Status", width=100)

        dt = FileDrop(self.list)
        self.list.SetDropTarget(dt)

        vbox.Add(self.st1, flag=wx.TOP | wx.BOTTOM, border=10)
        vbox.Add(self.list, 1, wx.EXPAND)
        hbox.Add(self.btnDownlaod, flag=wx.RIGHT, border=5)
        hbox.Add(self.btnReset, flag=wx.RIGHT, border=5)
        hbox.Add(self.btnQuit, flag=wx.RIGHT, border=5)
        vbox.Add(-1, 10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTRE)
        vbox.Add(-1, 10)
        panel.SetSizer(vbox)

        # event bindings
        self.Bind(wx.EVT_BUTTON, self.on_reset, self.btnReset)
        self.Bind(wx.EVT_BUTTON, self.on_quit, self.btnQuit)
        self.Bind(wx.EVT_BUTTON, self.on_download, self.btnDownlaod)
        self.Bind(wx.EVT_MENU, self.about, id=ID_ABOUTBOX)
        self.Bind(wx.EVT_MENU, self.change_account, id=ID_CHANGEACMENU)

        # window settings
        self.Centre()
        self.SetSize(600, 400)
        self.Show(True)

    def about(self, e):
        description = wordwrap(
            "Cross platform automated subtitle downloader, that uses movie file hash to identify and download subtitle",
            300,
            wx.ClientDC(self),
        )
        license = wordwrap("Released under MIT license", 300, wx.ClientDC(self))

        info = wx.adv.AboutDialogInfo()
        info.SetName("Easy Sub")
        info.SetVersion("2.1")
        info.SetDescription(description)
        info.SetLicense(license)
        info.AddDeveloper("Sadman Muhib Samyo")
        wx.adv.AboutBox(info)

    def change_account(self, e):
        dlg = ChangeAccountGUI(None, -1, "Account info")
        dlg.ShowModal()
        dlg.Destroy()

    def downloader(self):
        total_items = self.list.GetItemCount()
        print("Total Items", total_items)
        for item_index in range(total_items):
            path = self.list.GetItem(
                item_index, 0
            )  # gets the item (first column) from list control
            path = path.GetText()  # contains the path of the movie file
            # do some work with the path and do your download
            self.list.SetItem(item_index, 1, "Downloading")
            print("Getting inside try/catch")
            try:
                print("Inside Try")
                if self.sub_handler.search(path):
                    wx.CallAfter(
                        self.list.SetItem, item_index, 1, "OK"
                    )  # update the listcontrol for
                    print("Inside If")
                else:
                    wx.CallAfter(
                        self.list.SetItem, item_index, 1, "Not Found"
                    )  # update the listcontrol for
                    print("Inside else")
            except Exception as e:
                print("Inside Exception")
                wx.MessageBox("Error: %s" % e, "Error", wx.OK | wx.ICON_ERROR)
                self.list.SetItem(item_index, 1, "Error")
                return
        wx.MessageBox("All tasks completed", "EasySub", wx.OK | wx.ICON_INFORMATION)

    def on_download(self, e):
        Thread(target=self.downloader).start()

    def on_reset(self, e):
        self.list.DeleteAllItems()

    def on_quit(self, e):
        wait = wx.BusyInfo("Logging out...")
        self.auth.logout()
        del wait
        self.Destroy()
