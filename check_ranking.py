from googlesearch import search
import datetime
import pandas as pd
from urllib.error import HTTPError

class DataFrameHandler:

    def __init__(self, query="", domain="", filename=""):
        self.query = query
        self.domain = domain
        self.filename = filename
        self.ranking_dict = {}

    def search_term(self):

        try:
            # 日本語のGoogle検索を行う。言語は日本語。１ページあたりの検索数は10個,50個検索して止める。
            search_result_list = list(search(self.query, lang="jp", num=10, stop=50, pause=1))
        except HTTPError:
            return -1

        # URLリストをデータフレームに格納する
        df = pd.DataFrame(search_result_list, columns=["urls"])

        # サイト内URLを削除する
        clean_df = df[(~df.urls.str.contains("#"))].reset_index()

        # ドメインを検索
        index = clean_df[clean_df.urls.str.contains(self.domain)].index.to_list()

        if not index:
            rank = "50+"
        else:
            rank = index[0] + 1

        now = datetime.datetime.now()

        self.ranking_dict = {'SearchTerm': self.query,
                             'Ranking': rank,
                             'Pre': None,
                             'Diff': None,
                             'TargetSite': self.domain,
                             'Date': now.strftime("%Y/%m/%d %X")
                             }

        return

    def create(self):

        if self.search_term() == -1:
            print("Too Many Requests")
            return

        df = pd.DataFrame(self.ranking_dict, index=[0])
        df.to_pickle(self.filename)

    def add(self):

        if self.search_term() == -1:
            print("Too Many Requests")
            return

        df = pd.read_pickle(self.filename)

        add_df = pd.DataFrame(self.ranking_dict, index=[0])

        df = df.append(add_df)

        df.reset_index(drop=True, inplace=True)

        df.to_pickle(self.filename)

    def update(self, index):

        if self.search_term() == -1:
            print("Too Many Requests")
            return

        new = self.ranking_dict["Ranking"]

        df = pd.read_pickle(self.filename)
        pre = df.loc[index, "Ranking"]

        df.loc[index, "Ranking"] = new
        df.loc[index, "Pre"] = pre

        if (isinstance(new, int) == True) & (isinstance(pre, int) == True):
            df.loc[index, "Diff"] = pre - new
        else:
            df.loc[index, "Diff"] = None

        df.to_pickle(self.filename)

    def delete(self, index):

        df = pd.read_pickle(self.filename)

        df.drop(df.index[index], inplace=True)

        df.reset_index(inplace=True, drop=True)

        df.to_pickle(self.filename)

