import os
from config import *
from DomainRegisterGUI import DomainRegisterGUI
from RankCheckerGUI import RankCheckerGUI

if __name__ == "__main__":

    # アプリ起動時に設定ファイルの有無を確認
    # ない場合には初期画面へ
    # ある場合には設定ファイルを読み込み
    if not os.path.exists(SETTINGS_FILE):
        app = DomainRegisterGUI()
    else:
        settings = load_obj()
        app = RankCheckerGUI()
