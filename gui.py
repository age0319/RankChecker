import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import check_ranking

file_name = "ranking.pkl"

# ウインドウの作成
base = tk.Tk()
base.title("RankChecker")
base.geometry("700x300")

# テキストボックス(query)の設定
EditBox_query = tk.Entry(width=20)
EditBox_query.insert(tk.END, "最初に表示される文字列")
EditBox_query.pack()

# テキストボックス(ドメイン)の設定
EditBox_url = tk.Entry(width=20)
EditBox_url.insert(tk.END, "domain")
EditBox_url.pack()

# ツリービューの設定
tree = ttk.Treeview(base)

# 列を３列作る
tree["column"] = (1, 2, 3, 4, 5)
tree["show"] = "headings"

# ヘッダーテキスト
tree.heading(1, text="検索ワード")
tree.heading(2, text="ランキング")
tree.heading(3, text="数")
tree.heading(4, text="ドメイン")
tree.heading(5, text="時間")

# 列の幅
tree.column(1, width=200)
tree.column(2, width=50)
tree.column(3, width=50)
tree.column(4, width=200)
tree.column(5, width=200)

# ツリービューの設置
tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def refresh():
    # ツリービューの初期化
    for i in tree.get_children():
        tree.delete(i)

    # 保存したデータフレームの読み込み
    df = pd.read_pickle(file_name)

    # 全データ挿入
    for i in range(df.index.stop):
        tree.insert("", "end", values=(df['SearchTerm'][i], df['Ranking'][i], df['Total'][i],
                                       df['TargetSite'][i], df['Date'][i]))


# clickイベント
def query_click():
    # ドメインを取得
    your_site_domain = EditBox_url.get()
    # クエリーに入力された内容を取得
    query = EditBox_query.get()
    # ランキングを検索
    check_ranking.search_term(query, your_site_domain, file_name)
    # ツリービューの初期化
    refresh()


# ボタン
btn = tk.Button(base, text='検索', command=query_click)
btn.place(x=500, y=0)

refresh()

# GUIアプリの実行
base.mainloop()
