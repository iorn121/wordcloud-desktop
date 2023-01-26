import codecs
import os
import pprint
from glob import glob
from random import sample

import matplotlib.pyplot as plt
import MeCab
import pandas as pd
# GoogleDriveをマウント
# from google.colab import drive
# from wordcloud import WordCloud

# drive.mount('/content/drive')




class Comment2WordCloud:
    def __init__(self, csv_path, header=None):
        self.data = pd.read_csv(csv_path, header=None, encoding='utf-8')
        pprint.pprint(self.data)

    def wakati_count(self):
        # MeCabのTaggerオブジェクトを作成
        mecab = MeCab.Tagger()

        # 各文節をカウントするための辞書を用意する
        self.count_text = {}

        # カウントしない文節をsetで用意
        self.non_count = ("/", "", " ", "　", "、", "。", ".", "な", "を", "の", "さ", "で", "て", "せる", "だ",
                          "u3000", "た", "か", "ね", "ぞ", "か", "が", "まし", "も", "よ", "は", "き", "まし")

        # 各行を処理する
        for column_name, item in self.data.iteritems():
            # MeCabを使用して日本語の文字列を分かち書きにする
            for sentence in item:
                node = mecab.parseToNode(str(sentence))

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
        self.wordcloud = WordCloud(background_color="white", font_path='/usr/share/fonts/truetype/fonts-japanese-mincho.ttf',
                                   width=width, height=height, regexp=r"[0-9a-zA-Zぁ-んァ-ヶｱ-ﾝﾞﾟ一-龠ー]+").generate(self.count_words_text)

    def show_wordcloud(self, width=16, height=9):
        plt.figure(figsize=(width, height))
        plt.imshow(self.wordcloud)
        plt.axis("off")

    def save_wordcloud(self, save_path):
        plt.savefig(fname=save_path, bbox_inches='tight', pad_inches=0)


# 指定のフォルダ内のファイルを取得する
# files = glob('/content/drive/MyDrive/Colab Notebooks/data/*')
# output_path = '/content/drive/MyDrive/Colab Notebooks/output/'
# for file in files:
#     csv_path = file
#     file_name = os.path.splitext(os.path.basename(file))[0]
#     count_save_path = output_path+'count_sorted_'+file_name+'.txt'
#     wordcloud_save_path = output_path+'word_cloud_'+file_name+'.png'
#     # print(count_save_path)
#     # print(wordcloud_save_path)

#     c2wc = Comment2WordCloud(csv_path)

#     c2wc.wakati_count()
#     c2wc.save_count(count_save_path)
#     c2wc.create_wordcloud()
#     c2wc.show_wordcloud()
#     c2wc.save_wordcloud(wordcloud_save_path)
