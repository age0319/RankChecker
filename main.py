import check_ranking

query = 'ubuntu　インストール'
your_site_domain = 'https://ymgsapo.com'
file_name = "ranking.pkl"

print(__name__)


def start():
    check_ranking.add_update_pickle(query, your_site_domain, file_name)


if __name__ == '__main__':
    start()