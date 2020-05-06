import csv
from urllib.parse import urlparse
from googlesearch import search


# リストの中から自分のブログのドメインのインデックスを返す。
# 見つからなかった場合にはFalseを返す
def my_index(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default


def reg_ranking_by_query(query, your_site_domain):

    ranking_dict = {}
    ranking_dict['SearchTerm'] = query

    ## 日本語のGoogle検索を行う。言語は日本語。１ページあたりの検索数は10個,50個検索して止める。
    search_result_list = list(search(query, lang="jp", num=10, stop=50, pause=1))

    domain_list = []
    for index, url in enumerate(search_result_list):
        # URLのランキングを保存する
        if your_site_domain in url:
            # より上位の順位を登録する
            if "Ranking(URL)" not in ranking_dict.keys():
                ranking_dict["Ranking(URL)"] = index + 1
            else:
                pass
        # URLからドメインを抽出してリストに格納する
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        domain_list.append(domain)
        # print(index, url)

    # print(domain_list)

    # 重複を無くす
    unique_domain_list = list(dict.fromkeys(domain_list))

    # print(unique_domain_list)

    if my_index(unique_domain_list, your_site_domain) is not False:
        ranking = my_index(unique_domain_list, your_site_domain) + 1
        # print("Your site ranking is:", ranking, "!!!")
        ranking_dict['Ranking(Domain)'] = ranking
    else:
        # print("Hmm...Ranking Out")
        ranking_dict['Ranking(Domain)'] = -1

    # print(ranking_dict)

    return ranking_dict