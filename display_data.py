import pandas as pd
import os


def make_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def get_paper_list():
    database_dir_name = 'DATABASE'
    if os.path.exists(database_dir_name):
        dir_name = 'PAPERLIST'
        make_dir(dir_name)
        for root, dirs, files in os.walk(database_dir_name):
            for file_name in files:
                database_path = os.path.join(database_dir_name, file_name)
                store = pd.HDFStore(database_path)
                keys = store.keys()
                store.close()
                for key in keys:
                    df = pd.read_hdf(database_path, key)
                    df = df[['title', 'author', 'abstract', 'conference']]
                    pd.set_option('display.max_colwidth', -1)
                    file_name = key[1:] + '.html'
                    path = os.path.join(dir_name, file_name)
                    df.to_html(path, header=False)
                    # df.to_csv(file_name.split('.')[0] + '.csv', mode='a', encoding='utf_8_sig', index=False, header=False)

        print('OK!')
    else:
        print('No Database!')


# if __name__ == '__main__':
#     get_paper_list()
