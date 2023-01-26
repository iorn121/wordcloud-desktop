import os
import wx
import pandas as pd
from comment_analysys import Comment2WordCloud
import glob


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent=parent
        # 画像表示部分
        # bitで表現させる 'gazou.png'は、画像ファイルパスに置換して下さい。
        # bitmap = wx.Image('./word_cloud_当面の目標.png').ConvertToBitmap()
        # # イメージコントロールを配置
        # wx.StaticBitmap(parent=self,
        #                 bitmap=bitmap,
        #                 size=(1000,500)
        #                 )
        # self.SetClientSize(bitmap.GetSize())
        
        self.font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.output_path='./output/wordcloud.png'
        # bitで表現させる
        init_bitmap = wx.Image('./init.png').ConvertToBitmap()
        # イメージコントロールを配置
        self.result_img =wx.StaticBitmap(parent=self,bitmap=init_bitmap, size=(640, 480))


        # self.text_box = wx.TextCtrl(self, id=-1, value='BoxSizer下',style=wx.BORDER_NONE)
        # self.text_box.SetBackgroundColour('yellow')
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # ウィジェットを作る
        self.button_upload = wx.Button(self, -1, 'ファイルを開く')
        # 分かり易さのため、背景を青に設定
        self.button_upload.SetFont(self.font)
        # ウィジェットを作る
        self.text_filename = wx.TextCtrl(self, id=-1, value='aa')
        # 色の指定は、下記方法でもOK
        self.text_filename.SetBackgroundColour('#ff00ff')
        # ウィジェットを作る
        self.content = wx.TextCtrl(self, id=-1, value='aa')
        # 色の指定は、下記方法でもOK
        self.content.SetBackgroundColour('green')
        # 各ウィジェットをSizerにAdd　していく
        self.button_download = wx.Button(self, -1, '画像をダウンロード')
        # 分かり易さのため、背景を青に設定
        self.button_download.SetFont(self.font)
        grid_sizer.Add(self.button_upload, 1,wx.ALIGN_CENTER | wx.BOTTOM,10) 
        grid_sizer.Add(self.text_filename, 1, wx.EXPAND | wx.BOTTOM,10)
        grid_sizer.Add(self.content,11,wx.EXPAND | wx.BOTTOM,10)
        grid_sizer.Add(self.button_download, 1,wx.ALIGN_CENTER) 
        
        sizer.Add(self.result_img, 2,wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(grid_sizer, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        # BoxSizerにAddしていく
        # Panleの規定Sizerに指定
        self.SetSizer(sizer) 
        
        # box_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.SetSizer(box_sizer)
        # button = wx.Button(self, -1, 'Open File',pos=(0,0))
        # box_sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.button_upload.Bind(wx.EVT_BUTTON, self.OnBrowse)
        self.button_download.Bind(wx.EVT_BUTTON, self.OnSave)
        
    def OnBrowse(self, event):
        with wx.FileDialog(self, 'CSVファイルを選択してください',wildcard='*.csv',style=wx.FD_OPEN) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                pathname = dialog.GetPath()
                filename = os.path.basename(pathname) 
                self.text_filename.SetLabel(filename)
                c2wc=Comment2WordCloud(pathname)
                self.content.SetLabel(c2wc.get_data())
                c2wc.wakati_count()
                c2wc.create_wordcloud(width=640,height=480)
                self.wordcloud_img=c2wc.get_wordcloud()
                self.wordcloud_img.to_file(self.output_path)
                result_bitmap = wx.Image(self.output_path).ConvertToBitmap()
                self.result_img.SetBitmap(result_bitmap)
                # c2wc.save_wordcloud(wordcloud_save_path)
                event.Skip()
    
    def OnSave(self,event):
        with wx.FileDialog(self, 'ファイル名を入力してください',defaultDir=os.getcwd(), defaultFile="wordcloud",wildcard='*.png',style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            dialog.SetFilterIndex(2)
            if dialog.ShowModal() == wx.ID_OK:
                self.output_file = dialog.GetPath()
            # dialog.Destroy()



class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,id=-1, title="createWordCloud",size=(1000,560))
        MainPanel(self)
        self.Show()
        
                 # 「ファイル」のメニューを作成
        # f_menu = wx.Menu()
        # # 下記の第一引数は「メニューコマンド ID」 
        # # なんでもOKの場合、-1
        # f_menu.Append(-1, '新規作成')
        # f_menu.Append(-1, '保存')
        # f_menu.Append(-1, '終了')

        # # 「編集」のメニューを作成
        # s_menu = wx.Menu()
        # s_menu.Append(-1, '画像サイズ変更')
        # s_menu.Append(-1, 'グレーイメージ化')

        # # メニューバーを作成
        # m_bar = wx.MenuBar()
        # m_bar.Append(f_menu, 'ファイル')
        # m_bar.Append(s_menu, '編集')

        # # メニューバーをFrameに設定
        # self.SetMenuBar(m_bar)




if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
