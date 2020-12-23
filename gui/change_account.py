import wx


class ChangeAccountGUI(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(ChangeAccountGUI, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.st_info = wx.StaticText(
            panel, label="Type in your OpenSubtitles account info"
        )
        self.st_user = wx.StaticText(panel, label="Username/Email")
        self.st_pass = wx.StaticText(panel, label="Password")

        self.user_txt = wx.TextCtrl(panel, size=(200, -1))
        self.pass_txt = wx.TextCtrl(panel, size=(200, -1))
        self.btnConfirm = wx.Button(panel, label="OK", size=(60, 40))

        vbox.Add(-1, 10)
        vbox.Add(self.st_info, flag=wx.LEFT | wx.RIGHT, border=10)
        vbox.Add(-1, 10)
        vbox.Add(self.st_user, flag=wx.LEFT, border=10)
        vbox.Add(self.user_txt, flag=wx.LEFT, border=10)
        vbox.Add(-1, 10)
        vbox.Add(self.st_pass, flag=wx.LEFT, border=10)
        vbox.Add(self.pass_txt, flag=wx.LEFT, border=10)
        vbox.Add(-1, 10)
        centre_pos = int(vbox.GetMinSize()[0] / 2 - 30)
        vbox.Add(self.btnConfirm, flag=wx.LEFT, border=centre_pos)
        vbox.Add(-1, 10)
        panel.SetSizer(vbox)

        # event bindings
        self.Bind(wx.EVT_BUTTON, self.onConfirm, self.btnConfirm)
        # self.Bind(wx.EVT_CLOSE, self.OnExit)

        self.SetSize(vbox.GetMinSize()[0], vbox.GetMinSize()[1])
        vbox.Fit(self)
        self.Centre()
        self.Show(True)

    def onConfirm(self, e):
        username = self.user_txt.GetValue()
        password = self.pass_txt.GetValue()
        if username == "" or password == "":
            return
        string = "[username]=" + username + "\n" + "[password]=" + password
        print(string)

        with open("Login.txt", "w") as f:
            f.write(string)

        wx.MessageBox(
            "Account info updated. Please restart the program",
            "Info",
            wx.OK | wx.ICON_INFORMATION,
        )
        self.Destroy()

    def OnExit(self, e):
        self.Destroy()