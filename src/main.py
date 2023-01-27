import os
import wx
import pandas as pd
from pathlib import Path
import sys

import traceback
from glob import glob
from tabulate import tabulate
import matplotlib.pyplot as plt
import MeCab
from wordcloud import WordCloud






class Comment2WordCloud:
    def __init__(self, csv_path, header=None):
        self.__data = pd.read_csv(csv_path, header=None, encoding='utf-8')
        self.__data_string = tabulate(self.__data,tablefmt='simple', showindex=False)
        
        self.fpath =  glob('/Library/Fonts//*.ttf')[0] if os.name=="posix" else glob('C:\Windows\Fonts\*.ttf')[0] 
        
        # カウントしない文節をsetで用意
        self.non_count = set(["/", "", " ", "　", "、", "。", ".",  "せる", "まし", "まし","ます","てる","たら"])
        for i in range(12353, 12439):
            self.non_count.add(chr(i))
        
    def get_data(self):
        return self.__data_string
    
    def get_wordcloud(self):
        try:
            return self.__wordcloud
        except Exception("wordcloud not created"):
            return

    def wakati_count(self):
        # MeCabのTaggerオブジェクトを作成
        mecab = MeCab.Tagger()

        # 各文節をカウントするための辞書を用意する
        self.count_text = {}
        

        # 各行を処理する
        for col_name,item in self.__data.items():
            # MeCabを使用して日本語の文字列を分かち書きにする
            
            for sentence in item:

                node = mecab.parseToNode(str(sentence).replace('\u3000',''))

                # 分かち書きされた文字列から各文節をカウントする
                while node:

                    if node.surface not in self.non_count:  # 不要な文字列はカウントしない
                        # まだ辞書に登録されていない文節の場合は、新しく辞書に登録する
                        if node.surface not in self.count_text:
                            self.count_text[node.surface] = 1
                        # 既に登録されている文節の場合は、カウントを1増やす
                        else:
                            self.count_text[node.surface] += 1
                    node = node.next

        # カウント数の降順に並び替える
        self.count_sorted_text = sorted([[str(k), v] for (k, v) in self.count_text.items()], key=lambda x: -x[1])
        self.count_words_text = str(self.count_sorted_text).replace(' ', '')

    def save_count(self, save_path):
        # 保存する
        with open(save_path, mode='w',  encoding="utf-8-sig") as f:
            f.write(self.count_words_text)
        return self.count_sorted_text

    def create_wordcloud(self, width=1600, height=900):
        self.__wordcloud = WordCloud(background_color="white", font_path=self.fpath,
                                   width=width, height=height, regexp=r"[0-9a-zA-Zぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠ー]+").generate(self.count_words_text)

    def show_wordcloud(self, width=16, height=9):
        plt.figure(figsize=(width, height))
        plt.imshow(self.__wordcloud)
        plt.axis("off")

    def save_wordcloud(self, save_path,width,height):
        plt.figure(figsize=(width, height))
        plt.imshow(self.__wordcloud)
        plt.axis("off")
        plt.savefig(fname=save_path, bbox_inches='tight', pad_inches=0)

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent=parent

        
        self.font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        # self.output_path=resource_path('./output/wordcloud.png')
        self.output_path='./output/wordcloud.png'
        # bitで表現させる
        init_bitmap = wx.Image(resource_path('./img/init.png')).ConvertToBitmap()
        # init_bitmap = wx.Image('img/init.png').ConvertToBitmap()
        # イメージコントロールを配置
        self.result_img =wx.StaticBitmap(parent=self,bitmap=init_bitmap, size=(640, 480))
        

        self.path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))


        # self.text_box = wx.TextCtrl(self, id=-1, value='BoxSizer下',style=wx.BORDER_NONE)
        # self.text_box.SetBackgroundColour('yellow')
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # ウィジェットを作る
        self.button_upload = wx.Button(self, -1, 'ファイルを開く')
        self.button_upload.SetFont(self.font)
        self.button_upload.SetForegroundColour("#38b48b")
        # ウィジェットを作る
        self.text_filename = wx.TextCtrl(self, id=-1, value='ファイル名が表示されます')
        self.text_filename.SetBackgroundColour('#eeeeee')
        self.text_filename.SetFont(self.font)
        self.text_filename.Disable()
        self.text_filename.SetForegroundColour("#103327")
        # ウィジェットを作る
        self.content = wx.TextCtrl(self, id=-1, value='ファイルの内容が表示されます')
        self.content.SetBackgroundColour('#eeeeee')
        self.content.SetFont(self.font)
        self.content.Disable()
        self.content.SetForegroundColour("#103327")
        # ウィジェットを作る
        self.button_download = wx.Button(self, -1, '画像をダウンロード')
        self.button_download.SetFont(self.font)
        self.button_download.SetForegroundColour("#38b48b")
        self.button_download.Disable()
        
        grid_sizer.Add(self.button_upload, 1,wx.ALIGN_CENTER | wx.BOTTOM,10) 
        grid_sizer.Add(self.text_filename, 1, wx.EXPAND | wx.BOTTOM,10)
        grid_sizer.Add(self.content,12,wx.EXPAND | wx.BOTTOM,10)
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
                self.basename=filename.split('.')[0]
                self.c2wc=Comment2WordCloud(pathname)
                self.content.SetLabel(self.c2wc.get_data())
                self.c2wc.wakati_count()
                self.c2wc.create_wordcloud(width=640,height=480)
                self.wordcloud_img=self.c2wc.get_wordcloud()
                self.wordcloud_img.to_file(self.output_path)
                result_bitmap = wx.Image(self.output_path).ConvertToBitmap()
                self.result_img.SetBitmap(result_bitmap)
                self.button_download.Enable()
                # c2wc.save_wordcloud(wordcloud_save_path)
    
    def OnSave(self,event):
        with wx.FileDialog(self, 'ファイル名を入力してください',defaultDir=self.path_to_download_folder, defaultFile=self.basename+"_wordcloud",wildcard='*.png',style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = dialog.GetPath()
            try:
                self.wordcloud_img.to_file(pathname)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)



class MyFrame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(None,id=-1, title="createWordCloud",size=(1000,560),style=style)
        self.SetBackgroundColour("#91b5a9")
        MainPanel(self)
        
        icon = wx.Icon('./img/Jellyfish-Icon.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        self.Show()



if __name__ == '__main__':

    try:
        app = wx.App()
        frame = MyFrame()
        app.MainLoop()

    except Exception as e:
        message = list(traceback.TracebackException.from_exception(e).format())

        #出来るだけ確実に書き出したかったので、絶対パスを直接指定してみた
        path = '/Users/iori_watanabe/Downloads/error_message.txt'

        with open(path, mode='w') as f:
            for row in message:
                f.write(row)