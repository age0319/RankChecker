from urllib.parse import urlparse
from googlesearch import search

query = 'django 画像 アップロード'
your_site_domain = 'https://ymgsapo.com'

## 日本語のGoogle検索を行う。言語は日本語。１ページあたりの検索数は10個,50個検索して止める。
search_result_list = list(search(query, lang="jp", num=10, stop=50, pause=1))

domain_list=[]
for index, url in enumerate(search_result_list):
    # URLからドメインを抽出してリストに格納する
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    domain_list.append(domain)
    print(index,url)

print(domain_list)

# 重複を無くす
unique_domain_list = list(dict.fromkeys(domain_list))

print(unique_domain_list)


# リストの中から自分のブログのドメインのインデックスを返す。
# 見つからなかった場合にはFalseを返す
def my_index(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default


if my_index(unique_domain_list, your_site_domain) is not False:
    ranking = my_index(unique_domain_list, your_site_domain) + 1
    print("Your site ranking is:", ranking, "!!!")
else:
    print("Hmm...Ranking Out")
