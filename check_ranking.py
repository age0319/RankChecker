import os
from urllib.parse import urlparse
from googlesearch import search
import pandas as pd


# リストの中から自分のブログのドメインのインデックスを返す。
# 見つからなかった場合にはFalseを返す
def my_index(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default


def calc_ranking_by_query(query, your_site_domain):

    ranking_dict = {}
    ranking_dict['SearchTerm'] = query

    ## 日本語のGoogle検索を行う。言語は日本語。１ページあたりの検索数は10個,50個検索して止める。
    search_result_list = list(search(query, lang="jp", num=10, stop=50, pause=1))

    domain_list = []
    for index, url in enumerate(search_result_list):
        # URLのランキングを辞書に登録する
        if your_site_domain in url:
            # より上位の順位を登録する、最初に登場したドメインが含まれたURLを登録する
            if "Ranking(URL)" not in ranking_dict.keys():
                ranking_dict["Ranking(URL)"] = index + 1
        else:
            # 見つからなかった場合には-1を登録する
            ranking_dict["Ranking(URL)"] = -1

        # URLからドメインを抽出してリストに格納する
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        domain_list.append(domain)

    # ドメインの重複を無くす
    unique_domain_list = list(dict.fromkeys(domain_list))

    # サイトのドメインが見つかった場合は辞書に登録する
    if my_index(unique_domain_list, your_site_domain) is not False:
        ranking = my_index(unique_domain_list, your_site_domain) + 1
        ranking_dict['Ranking(Domain)'] = ranking
    # サイトのドメインが見つからなかった場合には-1を辞書に登録する
    else:
        ranking_dict['Ranking(Domain)'] = -1

    return ranking_dict


def add_update_pickle(query, your_site_domain, file_name):
    print("---start---:::", query)

    if os.path.exists(file_name):
        print(pd.read_pickle(file_name))

    # 初回検索の場合
    if not os.path.exists(file_name):
        # データフレームを新しく作って保存する
        print("Create")
        ranking_dict = calc_ranking_by_query(query, your_site_domain)
        df = pd.DataFrame({'SearchTerm': [query],
                           'Ranking(Domain)': ranking_dict['Ranking(Domain)'],
                           'Ranking(URL)': ranking_dict['Ranking(URL)']
                           }
                          )
        df.to_pickle(file_name)
    else:
        df = pd.read_pickle(file_name)
        # 該当する検索ワードが無かったら新しくデータフレームを作って追加する
        if df[df["SearchTerm"] == query].empty:
            # Add
            print("Add")
            ranking_dict = calc_ranking_by_query(query, your_site_domain)
            df2 = pd.DataFrame({'SearchTerm': [query],
                                'Ranking(Domain)': ranking_dict['Ranking(Domain)'],
                                'Ranking(URL)': ranking_dict['Ranking(URL)']
                                }
                               )
            df.append(df2, ignore_index=True).to_pickle(file_name)
        else:
            # 該当する検索ワードがあったらランキングを更新する
            # Update
            print("Update")
            index = df[df["SearchTerm"] == query].index
            ranking_dict = calc_ranking_by_query(query, your_site_domain)

            df.loc[index, 'Ranking(Domain)'] = ranking_dict['Ranking(Domain)']
            df.loc[index, 'Ranking(URL)'] = ranking_dict['Ranking(URL)']
            df.to_pickle(file_name)

    print("---finish---")
    print(pd.read_pickle(file_name))