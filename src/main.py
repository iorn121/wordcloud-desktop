import wx
import pandas as pd
from comment_analysys import Comment2WordCloud

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # 画像表示部分
        # bitで表現させる 'gazou.png'は、画像ファイルパスに置換して下さい。
        # bitmap = wx.Image('./word_cloud_当面の目標.png').ConvertToBitmap()
        # # イメージコントロールを配置
        # wx.StaticBitmap(parent=self,
        #                 bitmap=bitmap,
        #                 size=(1000,500)
        #                 )
        # self.SetClientSize(bitmap.GetSize())
        text_box = wx.TextCtrl(self, id=-1, value='BoxSizer下')
        text_box.SetBackgroundColour('yellow')
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(rows=3, cols=1, gap=(10, 10))
        
        # ウィジェットを作る
        text1 = wx.TextCtrl(self, id=-1, value='aa')
        # 分かり易さのため、背景を青に設定
        text1.SetBackgroundColour('blue')
        # ウィジェットを作る
        text2 = wx.TextCtrl(self, id=-1, value='aa')
        # 色の指定は、下記方法でもOK
        text2.SetBackgroundColour('#ff00ff')
        # ウィジェットを作る
        text3 = wx.TextCtrl(self, id=-1, value='aa')
        # 色の指定は、下記方法でもOK
        text3.SetBackgroundColour('green')
        # 各ウィジェットをSizerにAdd　していく
        grid_sizer.Add(text1, 1, wx.EXPAND) 
        grid_sizer.Add(text2, 1, wx.EXPAND)
        grid_sizer.Add(text3,1,wx.EXPAND)
        
        # BoxSizerにAddしていく
        sizer.Add(text_box, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        # Panleの規定Sizerに指定
        self.SetSizer(sizer) 
        
        # box_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.SetSizer(box_sizer)
        # button = wx.Button(self, -1, 'Open File',pos=(0,0))
        # box_sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # button.Bind(wx.EVT_BUTTON, self.OnBrowse)
        
    def OnBrowse(self, event):
        with wx.FileDialog(self, 'Select Image File',
                           wildcard='PNG files (*.csv)|*.csv',
                           style=wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                csv_path = dialog.GetPaths()[0]
                c2wc=Comment2WordCloud(csv_path)


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,id=-1, title="createWordCloud",size=(1000,500))
        MyPanel(self)
        self.Show()
        
        

    def open(self, event):
        dialog = wx.FileDialog(None, u"csvファイルを選択してください", style=wx.FD_OPEN)
        dialog.ShowModal()
        name = dialog.GetMessage()
        path = dialog.GetPath()
        df = self.read_file("name.csv", path)
        print(df)

    def read_file(self, name, path):
        df = pd.read_csv(path, encoding="cp932")
        return df


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
