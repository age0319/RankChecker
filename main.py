import os
import pandas as pd
import check_ranking

query = 'ubuntu　ipアドレス　固定'
your_site_domain = 'https://ymgsapo.com'
file_name = "ranking.pkl"

print("---start---:::", query)

if os.path.exists(file_name):
    print(pd.read_pickle(file_name))

# 初回検索の場合
if not os.path.exists(file_name):
    # Create
    print("Create")
    ranking_dict = check_ranking.reg_ranking_by_query(query, your_site_domain)
    df = pd.DataFrame({'SearchTerm': [query],
                       'Ranking(Domain)': ranking_dict['Ranking(Domain)'],
                       'Ranking(URL)': ranking_dict['Ranking(URL)']
                       }
                      )
    df.to_pickle(file_name)
else:
    df = pd.read_pickle(file_name)

    if df[df["SearchTerm"] == query].empty:
        # Add
        print("Add")
        ranking_dict = check_ranking.reg_ranking_by_query(query, your_site_domain)
        df2 = pd.DataFrame({'SearchTerm': [query],
                           'Ranking(Domain)': ranking_dict['Ranking(Domain)'],
                           'Ranking(URL)': ranking_dict['Ranking(URL)']
                           }
                          )
        df.append(df2, ignore_index=True).to_pickle(file_name)
    else:
        # Update
        print("Update")
        index = df[df["SearchTerm"] == query].index
        ranking_dict = check_ranking.reg_ranking_by_query(query, your_site_domain)

        df.loc[index, 'Ranking(Domain)'] = ranking_dict['Ranking(Domain)']
        df.loc[index, 'Ranking(URL)'] = ranking_dict['Ranking(URL)']
        df.to_pickle(file_name)

print("---finish---")
print(pd.read_pickle(file_name))