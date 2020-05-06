# 自由にコードで遊ぶためのプレイグラウンド

import os
import pandas as pd

# l = ['ben','car','apple','ben','car','dick']
#
# # 順番はランダムで、リストの重複を取り除く
# print(set(l))
# print(list(set(l)))
# #{'car', 'apple', 'ben', 'dick'}
# #['car', 'apple', 'ben', 'dick']
#
# # 順序を保持したまま、リストの重複を取り除く
# print((dict.fromkeys(l)))
# # リストにする
# print((list(dict.fromkeys(l))))
# #{'ben': None, 'car': None, 'apple': None, 'dick': None}
# #['ben', 'car', 'apple', 'dick']
#
#
# def my_index(l, x, default=False):
#     if x in l:
#         return l.index(x)
#     else:
#         return default
#
# print(my_index(l,"apple"))
# # 2
# print(my_index(l,"car"))
# # 1
# print(my_index(l,"oppai"))
# # False

query = "legpress"
file_name = "hoge.pkl"

print("---start---:::", query)

if os.path.exists(file_name):
    print(pd.read_pickle(file_name))

# 初回検索の場合
if not os.path.exists(file_name):
    # Create
    print("Create")
    df = pd.DataFrame({'ST': [query],
                       'RankA': 2,
                       'RankB': 3
                       }
                      )
    df.to_pickle(file_name)
else:
    df = pd.read_pickle(file_name)

    if df[df["ST"] == query].empty:
        # Add
        print("Add")
        new_df = pd.DataFrame({'ST': [query],
                           'RankA': 12,
                           'RankB': 33
                           }
                          )
        df.append(new_df, ignore_index=True).to_pickle(file_name)
    else:
        # Update
        print("Update")
        index = df[df["ST"] == query].index
        df.iloc[index, 1] = 2
        df.iloc[index, 2] = -1
        df.to_pickle(file_name)

print("---finish---")
print(pd.read_pickle(file_name))