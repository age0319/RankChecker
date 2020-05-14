import tkinter as tk
from config import *
from RankCheckerGUI import RankCheckerGUI
from PIL import Image, ImageTk


class DomainRegisterGUI:
    def __init__(self):

        self.base = tk.Tk()
        self.base.title("Launcher")

        # 画像を配置する
        load = Image.open(IMAGE_PATH)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.base, image=render)
        img.image = render
        img.pack()

        # ラベル
        label = tk.Label(self.base, text="順位を調べたいサイトのドメインを入力してください。(例:myblog.com)")
        label.pack()

        # テキストボックス
        self.entryBox = tk.Entry(master=self.base)
        self.entryBox.pack()



        # ラベル
        label = tk.Label(self.base, text="検索エンジンの言語を選んでください。")
        label.pack()

        self.var = tk.StringVar()
        r1 = tk.Radiobutton(self.base, text='Japanese', variable=self.var, value='jp')
        r1.pack()
        r2 = tk.Radiobutton(self.base, text='English', variable=self.var, value='en')
        r2.pack()

        # ドメインの登録ボタン
        self.button1 = tk.Button(
            master=self.base,
            text="登録する",
            width=15,
            bg="lightblue",
            command=self.register_domain
        )

        self.button1.pack()

        self.base.mainloop()

    def register_domain(self):

        lang = self.var.get()
        domain = self.entryBox.get()

        d = {
            "lang": lang,
            "domain": domain
             }

        save_obj(d)

        # self.base.destroy()
        # app = RankCheckerGUI(domain)