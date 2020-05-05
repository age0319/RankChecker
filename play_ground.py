## 自由にコードで遊ぶためのプレイグラウンド

l = ['ben','car','apple','ben','car','dick']

# 順番はランダムで、リストの重複を取り除く
print(set(l))
print(list(set(l)))
#{'car', 'apple', 'ben', 'dick'}
#['car', 'apple', 'ben', 'dick']

# 順序を保持したまま、リストの重複を取り除く
print((dict.fromkeys(l)))
# リストにする
print((list(dict.fromkeys(l))))
#{'ben': None, 'car': None, 'apple': None, 'dick': None}
#['ben', 'car', 'apple', 'dick']


def my_index(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default

print(my_index(l,"apple"))
# 2
print(my_index(l,"car"))
# 1
print(my_index(l,"oppai"))
# False