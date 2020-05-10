from googlesearch import search
import os
import datetime
import pandas as pd


class DataFrameHandler:

    def __init__(self, query="", domain="", filename=""):
        self.query = query
        self.domain = domain
        self.filename = filename
        self.ranking_dict = {}

    def search_term(self):

        # 日本語のGoogle検索を行う。言語は日本語。１ページあたりの検索数は10個,50個検索して止める。
        search_result_list = list(search(self.query, lang="jp", num=10, stop=50, pause=1))

        # URLリストをデータフレームに格納する
        df = pd.DataFrame(search_result_list, columns=["urls"])

        # サイト内URLを削除する
        clean_df = df[(~df.urls.str.contains("#"))].reset_index()

        # ドメインを検索
        index = clean_df[clean_df.urls.str.contains(self.domain)].index.to_list()

        if not index:
            rank = "Out of ranking"
            total = 0
        else:
            # インデックスに＋１をする
            rank = [n + 1 for n in index]
            total = len(rank)

        dt_now = datetime.datetime.now()

        self.ranking_dict = {'SearchTerm': self.query,
                             'Ranking': rank,
                             'Total': total,
                             'TargetSite': self.domain,
                             'Date': dt_now
                             }

    def add(self):

        self.search_term()

        data = pd.DataFrame(self.ranking_dict)

        if not os.path.exists(self.filename):
            df = pd.DataFrame()
        else:
            df = pd.read_pickle(self.filename)

        df = df.append(data)

        df.reset_index(drop=True, inplace=True)

        df.to_pickle(self.filename)

    def update(self, index):

        self.search_term()

        df = pd.read_pickle(self.filename)

        df.loc[index] = [self.query, self.ranking_dict["Ranking"], self.ranking_dict["Total"], self.domain,
                         self.ranking_dict["Date"]]

        df.to_pickle(self.filename)

    def delete(self, index):

        df = pd.read_pickle(self.filename)

        df.drop(df.index[index], inplace=True)

        df.reset_index(inplace=True, drop=True)

        df.to_pickle(self.filename)

