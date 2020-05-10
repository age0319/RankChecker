import tkinter as tk
from tkinter import ttk
import pandas as pd
from check_ranking import Search


class RankCheckerGUI:
    def __init__(self):
        self.filename = "ranking.pkl"
        self.domain = "ymgsapo.com"

        self.selected = []

        self.base = tk.Tk()
        self.base.title("RankChecker")
        self.base.geometry("800x800")

        # テキストボックス
        self.entryBox = tk.Entry(master=self.base)
        self.entryBox.pack()

        # ボタン
        self.button1 = tk.Button(
            master=self.base,
            text="Button",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.query_click  # クリックに実行する関数
        )
        self.button1.pack()

        # 削除ボタン
        self.button2 = tk.Button(
            master=self.base,
            text="Button",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.remove_click  # クリックに実行する関数
        )
        self.button2.pack()

        # TreeViewの設定
        self.tree = ttk.Treeview(self.base)

        # 列を作る
        self.tree["column"] = (1, 2, 3, 4, 5, 6)
        self.tree["show"] = "headings"

        # ヘッダーテキスト
        self.tree.heading(1, text="No.")
        self.tree.heading(2, text="検索ワード")
        self.tree.heading(3, text="ランキング")
        self.tree.heading(4, text="数")
        self.tree.heading(5, text="ドメイン")
        self.tree.heading(6, text="時間")

        # 列の幅
        self.tree.column(1, width=10)
        self.tree.column(2, width=100)
        self.tree.column(3, width=10)
        self.tree.column(4, width=10)
        self.tree.column(5, width=50)
        self.tree.column(6, width=50)

        # ツリービューの設置
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 選択されたTreeviewを取得するための関数をバインド
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_pkl_insert_treeview()

        self.base.mainloop()

    def on_tree_select(self, event):
        self.selected = []
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            self.selected.append(item_text[0])
        print(self.selected)

    def query_click(self):
        # 検索語を取得
        query = self.entryBox.get()

        # ランキングを検索
        sr = Search(query, self.domain, self.filename)
        sr.search_term()

        # ツリービューの削除
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.load_pkl_insert_treeview()

    def load_pkl_insert_treeview(self):
        # 保存したデータフレームの読み込み
        self.df = pd.read_pickle(self.filename)

        # 全データ挿入
        for i in range(self.df.index.stop):
            self.tree.insert("", "end", values=(i, self.df['SearchTerm'][i], self.df['Ranking'][i], self.df['Total'][i],
                                                self.df['TargetSite'][i], self.df['Date'][i]))

    def remove_click(self):

        print("hoge")
        # 保存したデータフレームの読み込み
        df = pd.read_pickle(self.filename)

        # strで取れるため、intへの変換が必要
        self.selected = list(map((lambda x: int(x)), self.selected))

        print(self.selected)

        df.drop(df.index[self.selected], inplace=True)
        df.reset_index(inplace=True, drop=True)
        df.to_pickle(self.filename)

        print(df)
        # ツリービューの削除
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.load_pkl_insert_treeview()


if __name__ == "__main__":
    app = RankCheckerGUI()