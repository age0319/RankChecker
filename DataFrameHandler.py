from googlesearch import search
import datetime
import pandas as pd
from urllib.error import HTTPError
from config import *


class DataFrameHandler:

    def __init__(self, query=""):

        settings = load_obj()

        self.query = query
        self.domain = settings["domain"]
        self.lang = settings["lang"]
        self.filename = RANKINGS_FILE
        self.ranking_dict = {}

    def search_term(self):

        try:
            # Google Search 10 urls per 1 page and stop by 50.
            search_result_list = list(search(self.query, lang=self.lang, num=10, stop=50, pause=1))
        except HTTPError:
            return -1

        # input urls to data frame.
        df = pd.DataFrame(search_result_list, columns=["urls"])

        # Delete # containing URLs.
        clean_df = df[(~df.urls.str.contains("#"))].reset_index()

        # Search Domain.
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

        new_rank = self.ranking_dict["Ranking"]

        df = pd.read_pickle(self.filename)
        pre_rank = df.loc[index, "Ranking"]

        df.loc[index, "Ranking"] = new_rank
        df.loc[index, "Pre"] = pre_rank
        df.loc[index, "Date"] = self.ranking_dict["Date"]

        if (isinstance(new_rank, int)) & (isinstance(pre_rank, int)):
            df.loc[index, "Diff"] = pre_rank - new_rank
        else:
            df.loc[index, "Diff"] = None

        df.to_pickle(self.filename)

    def delete(self, index):

        df = pd.read_pickle(self.filename)

        df.drop(df.index[index], inplace=True)

        df.reset_index(inplace=True, drop=True)

        df.to_pickle(self.filename)
