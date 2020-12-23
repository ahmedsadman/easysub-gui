import wx


class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        super(FileDrop, self).__init__()
        self.window = window
        # self.field = field

    def OnDropFiles(self, x, y, filenames):
        for i in filenames:
            index = self.window.InsertItem(0, i)
            print("Index is", index)
            self.window.SetItem(index, 1, "Waiting")
        return 0