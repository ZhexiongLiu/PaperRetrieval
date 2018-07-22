#!/usr/bin/python3
from argparse import ArgumentParser
import urllib.request
import pandas as pd
import re
import os
import datetime
from time import sleep


def make_dir():
    if not os.path.exists('DATABASE'):
        os.makedirs('DATABASE')


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


def parse_content(content, name, label, year):
    author_list = []
    abstract_list = []
    pattern1 = re.compile(r'<dt class="ptitle"><br><a href="(.*?)">(.*?)</a></dt>')
    pattern2 = re.compile(r'\[<a href="(.*?)">pdf</a>\]')
    items1 = re.findall(pattern1, content)
    items2 = re.findall(pattern2, content)

    df1 = pd.DataFrame(items1, columns=['html', 'title'])
    df2 = pd.DataFrame(items2, columns=['pdf'])
    df1['html'] = ['http://openaccess.thecvf.com/' + i for i in df1['html']]
    df2['pdf'] = ['http://openaccess.thecvf.com/' + i for i in df2['pdf']]
    for i in range(len(df1)):
        title = df1.title[i]
        html_url = df1.html[i]
        print(label + ' ' + str(i) + ': ' + title)
        content = get_content(html_url, year)
        author, abstract = parse_sub_content(content)
        author_list.append(author)
        abstract_list.append(abstract)

    df = pd.concat([df1, df2], axis=1)
    df['author'] = pd.Series(author_list)
    df['abstract'] = pd.Series(abstract_list)
    df['conference'] = label
    file_name = name + '.h5'
    df.to_hdf(os.path.join('DATABASE', file_name), key=label)


def parse_sub_content(content):
    pattern1 = re.compile(r'<br><b><i>(.*?)</i></b>')
    pattern2 = re.compile(r'<br><br><div id="abstract" >\n(.*?)</div>')
    author = re.findall(pattern1, content)
    abstract = re.findall(pattern2, content)
    if len(author) > 0 and len(abstract) > 0:
        return author[0], abstract[0]
    else:
        return 'NaN', 'NaN'


def init_database():
    base_url = 'http://openaccess.thecvf.com/'
    this_year = datetime.datetime.today().year
    conference_year = list(range(this_year, 2012, -1))
    conference_name = ['CVPR', 'ICCV']
    make_dir()
    for name in conference_name:
        for year in conference_year:
            if year % 2 == 0 and name == 'ICCV':
                continue
            label = '{}{}'.format(name, year)
            url = base_url + '{}.py'.format(label)
            print('\n----------- Fetching {}{} Data -----------\n'.format(name, year))
            content = get_content(url, year)
            parse_content(content, name, label, year)


# if __name__ == '__main__':
#     init_database()
