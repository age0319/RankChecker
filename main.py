import os
from config import *
from DomainRegisterGUI import DomainRegisterGUI
from RankCheckerGUI import RankCheckerGUI

if __name__ == "__main__":

    if not os.path.exists(SETTINGS_FILE):
        app = DomainRegisterGUI()
    else:
        with open(SETTINGS_FILE, 'r') as f:
            domain = f.readlines()

        app = RankCheckerGUI(domain[0].rstrip())