import pickle

SETTINGS_FILE = "data/settings.pkl"
RANKINGS_FILE = "data/rankings.pkl"
IMAGE_PATH = "icon/ranking-icon.png"


def save_obj(obj):
    with open(SETTINGS_FILE, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj():
    with open(SETTINGS_FILE, 'rb') as f:
        return pickle.load(f)
