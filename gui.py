import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import check_ranking

your_site_domain = 'https://ymgsapo.com'

# 保存したデータフレームの読み込み
file_name = "ranking.pkl"
df = pd.read_pickle(file_name)

# ウインドウの作成
base = tk.Tk()
base.title("RankChecker")
base.geometry("400x300")

# テキストボックスの設定
EditBox = tk.Entry(width=20)
EditBox.insert(tk.END, "最初に表示される文字列")
EditBox.pack()

# ツリービューの設定
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

# ツリービューの設置
tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def refresh():
    # ツリービューの初期化
    for i in tree.get_children():
        tree.delete(i)

    # 保存したデータフレームの読み込み
    df2 = pd.read_pickle(file_name)

    # 全データ挿入
    for i in range(df2.index.stop):
        tree.insert("", "end", values=(df2['SearchTerm'][i], df2['Ranking(Domain)'][i], df2['Ranking(URL)'][i]))


# clickイベント
def query_click():
    # エントリーに入力された内容を取得
    query = EditBox.get()
    # ランキングを検索
    check_ranking.add_update_pickle(query, your_site_domain, file_name)
    # ツリービューの初期化
    refresh()


# ボタン
btn = tk.Button(base, text='検索', command=query_click)
btn.place(x=300, y=0)

# GUIアプリの実行
base.mainloop()
