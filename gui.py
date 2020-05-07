import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd

file_name = "ranking.pkl"

df = pd.read_pickle(file_name)

base = tk.Tk()
base.title("RankChecker")
base.geometry("400x300")

tree = ttk.Treeview(base)

# 列を３列作る
tree["column"] = (1, 2, 3)
tree["show"] = "headings"

# ヘッダーテキスト
tree.heading(1, text="検索ワード")
tree.heading(2, text="ランキング(ドメイン)")
tree.heading(3, text="ランキング（URL）")
# 列の幅
tree.column(1, width=200)
tree.column(2, width=100)
tree.column(3, width=100)

# データ挿入
for i in range(df.index.stop):
    tree.insert("", "end", values=(df['SearchTerm'][i], df['Ranking(Domain)'][i], df['Ranking(URL)'][i]))

# 設置
tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

base.mainloop()