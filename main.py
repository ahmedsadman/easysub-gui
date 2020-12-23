import wx
from gui import GUI


def main():
    app = wx.App()
    GUI(
        None,
        -1,
        "Easy Sub",
        style=wx.STAY_ON_TOP | wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX,
    )
    app.MainLoop()


if __name__ == "__main__":
    main()