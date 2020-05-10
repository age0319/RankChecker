import tkinter as tk
from tkinter import ttk
import pandas as pd
from check_ranking import DataFrameHandler


class RankCheckerGUI:
    def __init__(self):
        self.filename = "ranking.pkl"
        self.domain = "ymgsapo.com"

        self.selected_no = []
        self.selected_query = []

        self.base = tk.Tk()
        self.base.title("RankChecker")
        self.base.geometry("800x800")

        # テキストボックス
        self.entryBox = tk.Entry(master=self.base)
        self.entryBox.pack()

        # 追加ボタン
        self.button1 = tk.Button(
            master=self.base,
            text="追加",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.add_click  # クリックに実行する関数
        )
        self.button1.pack()

        # 削除ボタン
        self.button2 = tk.Button(
            master=self.base,
            text="削除",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.delete_click  # クリックに実行する関数
        )
        self.button2.pack()

        # 更新ボタン
        self.button3 = tk.Button(
            master=self.base,
            text="更新",  # 初期値
            width=15,  # 幅
            bg="lightblue",  # 色
            command=self.update_click  # クリックに実行する関数
        )
        self.button3.pack()

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
        self.selected_no = []
        self.selected_query = []

        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            self.selected_no.append(int(item_text[0]))
            self.selected_query.append(item_text[1])

    def load_pkl_insert_treeview(self):
        # 保存したデータフレームの読み込み
        df = pd.read_pickle(self.filename)

        # 全データ挿入
        for i in df.index:
            self.tree.insert("", "end", values=(i, df['SearchTerm'][i], df['Ranking'][i], df['Total'][i],
                                                df['TargetSite'][i], df['Date'][i]))

    def add_click(self):
        # 検索語を取得
        query = self.entryBox.get()

        # ランキングを検索
        handler = DataFrameHandler(query, self.domain, self.filename)
        handler.add()

        self.refresh()

    def delete_click(self):

        handler = DataFrameHandler(filename=self.filename)
        handler.delete(self.selected_no)

        self.refresh()

    def update_click(self):

        handler = DataFrameHandler(self.selected_query[0], self.domain, self.filename)
        handler.update(self.selected_no[0])

        self.refresh()

    def refresh(self):
        # ツリービューの削除
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.load_pkl_insert_treeview()


if __name__ == "__main__":
    app = RankCheckerGUI()