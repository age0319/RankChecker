from googlesearch import search
import pandas as pd
import os
import datetime


def search_term(query, target_site_domain, file_name):

    ## 日本語のGoogle検索を行う。言語は日本語。１ページあたりの検索数は10個,50個検索して止める。
    search_result_list = list(search(query, lang="jp", num=10, stop=50, pause=1))
    df = pd.DataFrame(search_result_list, columns=["urls"])

    ## 重複を消す
    clean_df = df[(~df.urls.str.contains("#"))].reset_index()

    ## ドメインを検索
    index = clean_df[clean_df.urls.str.contains(target_site_domain)].index.to_list()

    ## インデックスに＋１をしてランキングにする
    rank = [n + 1 for n in index]

    dt_now = datetime.datetime.now()

    data = pd.DataFrame({'SearchTerm': query,
                         'Ranking': [rank],
                         'Total': len(rank),
                         'TargetSite': target_site_domain,
                         'Date': dt_now
                         }
                        )

    if not os.path.exists(file_name):
        df = pd.DataFrame()
    else:
        df = pd.read_pickle(file_name)

    df = df.append(data)
    df.reset_index(drop=True, inplace=True)
    print(df)
    df.to_pickle(file_name)

    return
