#!/usr/bin/python3
import urllib.request
import pandas as pd
import datetime
import re
import os


def make_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def read_data(name, label):
    try:
        df = pd.read_hdf(os.path.join('DATABASE', name + '.h5'), '/' + label)
        return df
    except Exception as e:
        print('---------------- No {} Data In The Database, Please Update.'.format(label))
        return None


def get_pdf_file(url, label, dir_name, file_name):
    file_name = label + ' ' + file_name + '.pdf'
    file_name = file_name.replace(':', '')
    url_request = urllib.request.urlopen(url, timeout=20)
    pdf_file = url_request.read()

    path = os.path.join(dir_name, file_name)
    fid = open(path, 'wb')
    fid.write(pdf_file)
    fid.close()
    print('Downloaded File: ' + file_name)


def generate_abstract(author, title, abstract, label, dir_name, file_name):
    file_name = file_name + '.txt'
    path = os.path.join(dir_name, file_name)
    with open(path, 'a+') as f:
        f.write(title + '\n')
        f.write(author + '; ' + label + '\n\n')
        f.write(abstract + '\n\n\n')


def index_word(df, key_word_list, mode):
    if mode == 1:
        df['temp_col'] = df['title'] + df['abstract']
    elif mode == 2:
        df['temp_col'] = df['title'] + df['abstract'] + df['author']
    else:
        df['temp_col'] = df['title']

    for word in key_word_list:
        df = df[df['temp_col'].str.match(re.compile(r'.*?(\b){}(\b).*'.format(word), re.IGNORECASE), na=False)]
        # df = df[rex in df.title]
    df = df.reset_index()
    return df


def get_paper(name, period, key_word_list, mode):
    this_year = datetime.datetime.today().year
    year_list = []
    make_dir(name)
    dir_name = name
    for i in range(period):
        if this_year - i >= 2013:
            year_list.append(this_year - i)
    for year in year_list:
        label = name + str(year)
        df = read_data(name, label)
        if df is None:
            continue
        if key_word_list is not None:
            df = index_word(df, key_word_list, mode)

        for i in range(len(df)):
            pdf_url = df.loc[i, 'pdf']
            author = df.loc[i, 'author']
            title = df.loc[i, 'title']
            abstract = df.loc[i, 'abstract']
            file_name = title
            get_pdf_file(pdf_url, label, dir_name, file_name)
            file_name = 'ABSTRACT'
            generate_abstract(author, title, abstract, label, dir_name, file_name)
