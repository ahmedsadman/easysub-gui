import wx
import sys
import time
import subtitle_handler
from threading import Thread
from wx.adv import AboutBox
from wx.adv import AboutDialogInfo
from wx.lib.wordwrap import wordwrap
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class FileDrop(wx.FileDropTarget):
	def __init__(self, window):
		super(FileDrop, self).__init__()
		self.window = window
		#self.field = field
	
	def OnDropFiles(self, x, y, filenames):
		for i in filenames:
			index = self.window.InsertItem(sys.maxint, i)
			self.window.SetItem(index, 1, 'Waiting')
		return 0


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
		ListCtrlAutoWidthMixin.__init__(self)


class ChangeAccountGUI(wx.Dialog):
	def __init__(self, *args, **kwargs):
		super(ChangeAccountGUI, self).__init__(*args, **kwargs)
		self.InitUI()

	def InitUI(self):
		panel = wx.Panel(self, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)

		self.st_info = wx.StaticText(panel, label='Type in your OpenSubtitles account info')
		self.st_user = wx.StaticText(panel, label='Username/Email')
		self.st_pass = wx.StaticText(panel, label='Password')

		self.user_txt = wx.TextCtrl(panel, size=(200, -1))
		self.pass_txt = wx.TextCtrl(panel, size=(200, -1))
		self.btnConfirm = wx.Button(panel, label='OK', size = (60, 40))

		vbox.Add(-1, 10)
		vbox.Add(self.st_info, flag = wx.LEFT | wx. RIGHT, border = 10)
		vbox.Add(-1, 10)
		vbox.Add(self.st_user, flag = wx.LEFT, border = 10)
		vbox.Add(self.user_txt, flag = wx.LEFT, border = 10)
		vbox.Add(-1, 10)
		vbox.Add(self.st_pass, flag = wx.LEFT, border = 10)
		vbox.Add(self.pass_txt, flag = wx.LEFT, border = 10)
		vbox.Add(-1, 10)
		centre_pos = vbox.GetMinSize()[0]/2 - 30
		vbox.Add(self.btnConfirm, flag = wx.LEFT, border = centre_pos)
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
		if username == '' or password == '':
			return
		string = '[username]=' + username + '\n' + '[password]=' + password
		print string

		with open("Login.txt", "w") as f:
			f.write(string)

		wx.MessageBox("Account info updated. Please restart the program", 'Info', wx.OK | wx.ICON_INFORMATION)
		self.Destroy()

	def OnExit(self, e):
		self.Destroy()

class GUI(wx.Frame):
	def __init__(self, *args, **kwargs):
		#wx.Frame.__init__(self, parent, id, title, size=(380, 230))
		super(GUI, self).__init__(*args, **kwargs)
		self.font = wx.Font(pointSize = 10, family = wx.DEFAULT, style = wx.NORMAL, weight = wx.BOLD)
		self.handler = subtitle_handler.MainEngine() 
		wait = wx.BusyInfo("Logging in, please wait...")

		try:
			self.token = self.handler.getToken() # login the user
		except:
			del wait
			wx.MessageBox("Login failed. Please check internet connection", "Login Error", wx.OK | wx.ICON_ERROR)
			sys.exit(-1)
		del wait

		if not self.token:
			print 'login error'
			wx.MessageBox("Cannot login with the provided username/pass combination.\nPlease type in your account info in the next window", 'Error', wx.OK | wx.ICON_ERROR)
			dlg = ChangeAccountGUI(None, -1, 'Account Info')
			dlg.ShowModal()
			try:
				dlg.Destroy()
			except:
				pass
			self.Destroy()

		self.initUI()

	def initUI(self):
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		panel = wx.Panel(self, -1)
		ID_ABOUTBOX = wx.NewId()
		ID_CHANGEACMENU = wx.NewId()

		# menu bar
		menubar = wx.MenuBar()
		menu = wx.Menu()
		menu.Append(ID_CHANGEACMENU, 'Account info')
		menu.Append(ID_ABOUTBOX, 'About')

		menubar.Append(menu, '&Menu')
		self.SetMenuBar(menubar)

		self.st1 = wx.StaticText(panel, label='Drag && Drop movie files below')
		self.st1.SetFont(self.font)

		self.btnDownlaod = wx.Button(panel, label='Download', size = (90, 40))
		self.btnReset = wx.Button(panel, label='Reset', size = (90, 40))
		self.btnQuit = wx.Button(panel, label='Quit', size = (90, 40))

		self.list = AutoWidthListCtrl(panel)
		self.list.InsertColumn(0, 'File', width=420)
		self.list.InsertColumn(1, 'Status', width=100)

		dt = FileDrop(self.list)
		self.list.SetDropTarget(dt)

		vbox.Add(self.st1, flag = wx.TOP | wx.BOTTOM, border = 10)
		vbox.Add(self.list, 1, wx.EXPAND)
		hbox.Add(self.btnDownlaod, flag = wx.RIGHT, border = 5)
		hbox.Add(self.btnReset, flag = wx.RIGHT, border = 5)
		hbox.Add(self.btnQuit, flag = wx.RIGHT, border = 5)
		vbox.Add(-1, 10)
		vbox.Add(hbox, flag = wx.ALIGN_CENTRE)
		vbox.Add(-1, 10)
		panel.SetSizer(vbox)

		# event bindings
		self.Bind(wx.EVT_BUTTON, self.onReset, self.btnReset)
		self.Bind(wx.EVT_BUTTON, self.onQuit, self.btnQuit)
		self.Bind(wx.EVT_BUTTON, self.onDownload, self.btnDownlaod)
		self.Bind(wx.EVT_MENU, self.About, id=ID_ABOUTBOX)
		self.Bind(wx.EVT_MENU, self.ChangeAC, id=ID_CHANGEACMENU)

		# window settings
		self.Centre()
		self.SetSize(600, 400)
		self.Show(True)

	def About(self, e):
		description = wordwrap("Cross platform automated subtitle downloader, that uses movie file hash to identify and download subtitle", 300, wx.ClientDC(self))
		license = wordwrap("Released under MIT license", 300, wx.ClientDC(self))

		info = wx.adv.AboutDialogInfo()
		info.SetName("Easy Sub")
		info.SetVersion("2.0")
		info.SetDescription(description)
		info.SetLicense(license)
		info.AddDeveloper("Sadman Muhib Samyo")
		wx.adv.AboutBox(info)

	def ChangeAC(self, e):
		dlg = ChangeAccountGUI(None, -1, 'Account info')
		dlg.ShowModal()
		dlg.Destroy()

	def Downloader(self):
		total_items = self.list.GetItemCount()
		for item_index in range(total_items):
			path = self.list.GetItem(item_index, 0) # gets the item (first column) from list control
			path = path.GetText() # contains the path of the movie file
			# do some work with the path and do your download
			self.list.SetItem(item_index, 1, 'Downloading')

			try:
				if self.handler.subSearch(path):
					wx.CallAfter(self.list.SetItem, item_index, 1, 'OK') # update the listcontrol for 
				else:
					wx.CallAfter(self.list.SetItem, item_index, 1, 'Not Found') # update the listcontrol for 
			except Exception, e:
				wx.MessageBox("Error: %s" % e, "Error", wx.OK | wx.ICON_ERROR)
				self.list.SetItem(item_index, 1, 'Error')
				return
		wx.MessageBox("All tasks completed", "EasySub", wx.OK | wx.ICON_INFORMATION)

	def onDownload(self, e):
		Thread(target=self.Downloader).start()

	def onReset(self, e):
		self.list.DeleteAllItems()

	def onQuit(self, e):
		wait = wx.BusyInfo("Logging out...")
		try:
			self.handler.logout(self.token)
		except:
			pass
		del wait
		self.Destroy()
	

def main():
	app = wx.App()
	GUI(None, -1, 'Easy Sub', style=wx.STAY_ON_TOP | wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
	app.MainLoop()


if __name__ == "__main__":
	main()