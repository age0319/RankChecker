import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import ImageTk, Image

from DataFrameHandler import DataFrameHandler
from config import *


class RankCheckerGUI:

    def __init__(self):

        self.counter = 0
        self.selected_no = []
        self.selected_query = []

        self.base = tk.Tk()
        self.tree = ttk.Treeview(self.base)
        self.entryBox = tk.Entry(self.base)

        self.labeltext = ""
        self.labeltext2 = ""

        self.window = None
        self.lang = None
        self.entryBox2 = None

    def main_window(self):

        self.base.title("RankChecker")
        self.base.geometry("800x800")

        # 設定ボタン
        button4 = tk.Button(
            master=self.base,
            text="設定",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.setting_window  # クリックに実行する関数
        )

        button4.pack()

        settings = load_obj()

        self.labeltext = settings["domain"]
        self.labeltext2 = settings["lang"]

        # ラベル
        label = tk.Label(self.base, text="【" + self.labeltext + "】の順位を調べます。")
        label.pack()

        label2 = tk.Label(self.base, text="検索エンジンの言語【" + self.labeltext2 + "】")
        label2.pack()

        # テキストボックス
        self.entryBox.pack()

        # 追加ボタン
        button1 = tk.Button(
            master=self.base,
            text="追加",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.add_click  # クリックに実行する関数
        )
        button1.pack()

        # 削除ボタン
        button2 = tk.Button(
            master=self.base,
            text="削除",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.delete_click  # クリックに実行する関数
        )
        button2.pack()

        # 更新ボタン
        button3 = tk.Button(
            master=self.base,
            text="更新",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.update_click  # クリックに実行する関数
        )
        button3.pack()

        # TreeViewの設定

        # 列を作る
        self.tree["column"] = (1, 2, 3, 4, 5, 6, 7)
        self.tree["show"] = "headings"

        # ヘッダーテキスト
        self.tree.heading(1, text="No.")
        self.tree.heading(2, text="検索ワード")
        self.tree.heading(3, text="ランキング")
        self.tree.heading(4, text="前回")
        self.tree.heading(5, text="差分")
        self.tree.heading(6, text="ドメイン")
        self.tree.heading(7, text="時間")

        # 列の幅
        self.tree.column(1, width=10)
        self.tree.column(2, width=100)
        self.tree.column(3, width=10)
        self.tree.column(4, width=10)
        self.tree.column(5, width=50)
        self.tree.column(6, width=50)
        self.tree.column(7, width=50)

        # ツリービューの設置
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 選択されたTreeviewを取得するための関数をバインド
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_pkl_insert_treeview()

        self.base.mainloop()

    def update_label(self):
        # 以下を見て解決すべし
        # https://stackoverflow.com/questions/17125842/changing-the-text-on-a-label
        settings = load_obj()

        self.labeltext = settings["domain"]
        self.labeltext2 = settings["lang"]

    def on_tree_select(self):
        self.selected_no = []
        self.selected_query = []

        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            self.selected_no.append(int(item_text[0]))
            self.selected_query.append(item_text[1])

    def load_pkl_insert_treeview(self):

        if not os.path.exists(RANKINGS_FILE):
            return

        # 保存したデータフレームの読み込み
        df = pd.read_pickle(RANKINGS_FILE)

        if df.empty:
            return

        for i in df.index:
            diff = df.loc[i, "Diff"]

            color = ""
            if diff is None:
                pass
            elif isinstance(diff, str):
                pass
            elif diff > 0:
                color = "green"
            elif diff < 0:
                color = "red"

            self.tree.insert("", "end", values=(i, df['SearchTerm'][i], df['Ranking'][i], df['Pre'][i], df['Diff'][i],
                                     df['TargetSite'][i], df['Date'][i]), tags=color)

        self.tree.tag_configure("red", foreground='red')
        self.tree.tag_configure("green", foreground='green')

    def add_click(self):

        # 検索語を取得
        query = self.entryBox.get()

        # ランキングを検索
        handler = DataFrameHandler(query)

        if not os.path.exists(RANKINGS_FILE):
            print("This is the 1st Search")
            handler.create()
        else:
            handler.add()

        self.entryBox.delete(0, 'end')

        self.refresh()

    def delete_click(self):

        handler = DataFrameHandler()
        handler.delete(self.selected_no)

        self.refresh()

    def update_click(self):

        handler = DataFrameHandler(self.selected_query[0])
        handler.update(self.selected_no[0])

        self.refresh()

    def refresh(self):
        # ツリービューの削除
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.load_pkl_insert_treeview()

    def setting_window(self):

        self.counter += 1

        self.window = tk.Toplevel(self.base)
        self.window.wm_title("Window #%s" % self.counter)

        # 画像を配置する
        load = Image.open(IMAGE_PATH)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.window, image=render)
        img.image = render
        img.pack()

        # ラベル
        label = tk.Label(self.window, text="順位を調べたいサイトのドメインを入力してください。(例:myblog.com)")
        label.pack()

        # テキストボックス
        self.entryBox2 = tk.Entry(self.window)
        self.entryBox2.pack()

        # ラベル
        label = tk.Label(self.window, text="検索エンジンの言語を選んでください。")
        label.pack()

        self.lang = tk.StringVar()
        r1 = tk.Radiobutton(self.window, text='Japanese', variable=self.lang, value='jp')
        r1.pack()
        r2 = tk.Radiobutton(self.window, text='English', variable=self.lang, value='en')
        r2.pack()

        # ドメインの登録ボタン
        button = tk.Button(
            master=self.window,
            text="登録する",
            width=15,
            bg="lightblue",
            command=self.register_setting
        )

        button.pack()

    def register_setting(self):

        lang = self.lang.get()
        domain = self.entryBox2.get()

        setting = {
            "lang": lang,
            "domain": domain
             }

        save_obj(setting)

        self.window.destroy()

        self.update_label()



