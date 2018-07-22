#!/usr/bin/python3
from argparse import ArgumentParser
import urllib.request
import pandas as pd
import re
import os


def make_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def get_pdf_file(url, dir_name, file_name):
    file_name = file_name + '.pdf'
    file_name = file_name.replace(':', '')
    url_request = urllib.request.urlopen(url, timeout=20)
    pdf_file = url_request.read()
    path = os.path.join(dir_name, file_name)
    with open(path, 'wb') as f:
        f.write(pdf_file)
        print('Downloaded File: ' + file_name)


def get_content(url, year):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request, timeout=20)
        if year >= 2018:
            content = response.read().decode('utf-8')
        else:
            content = response.read().decode('windows-1252')
    except Exception as e:
        print(e)
        sleep(10)
        content = ''
    return content


def parse_content(content):
    pattern1 = re.compile(r'<dt class="ptitle"><br><a href="(.*?)">(.*?)</a></dt>')
    pattern2 = re.compile(r'\[<a href="(.*?)">pdf</a>\]')
    items1 = re.findall(pattern1, content)
    items2 = re.findall(pattern2, content)

    df1 = pd.DataFrame(items1, columns=['html', 'title'])
    df2 = pd.DataFrame(items2, columns=['pdf'])
    df1['html'] = ['http://openaccess.thecvf.com/' + i for i in df1['html']]
    df2['pdf'] = ['http://openaccess.thecvf.com/' + i for i in df2['pdf']]
    df = pd.concat([df1, df2], axis=1)
    return df


def index_word(df, key_word_list):
    for word in key_word_list:
        df = df[df['title'].str.match(re.compile(r'.*?(\b){}(\b).*'.format(word), re.IGNORECASE))]
    df = df.reset_index()
    return df


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('name', type=str, choices=['CVPR, ICCV', 'cvpr', 'iccv'],
                        help='Input the name of the conference')
    parser.add_argument('year', type=int,
                        help='Input the year of the conference')
    parser.add_argument('-k', '--keyword', type=str, nargs='+',
                        help='Input search keywords, using space to split words')
    return parser.parse_args()


def main():
    args = parse_args()
    name = args.name.upper()
    year = args.year
    key_word_list = args.keyword

    base_url = 'http://openaccess.thecvf.com/'
    dir_name = name + 'LITE'
    make_dir(dir_name)

    url = base_url + '/{}{}.py'.format(name, year)
    content = get_content(url, year)
    df = parse_content(content)
    if key_word_list is not None:
        df = index_word(df, key_word_list)
    for i in range(len(df)):
        try:
            title = df.loc[i, 'title']
            pdf_url = df.loc[i, 'pdf']
            file_name = title
            get_pdf_file(pdf_url, dir_name, file_name)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
