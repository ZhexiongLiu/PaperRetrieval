#!/usr/bin/python3
from display_data import get_paper_list
from search_data import get_paper
from fetch_data import init_database
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-r', '--restore', action='store_true',
                        help='Restore the local database. PLEASE SET IT ONLY IF NEW CONFERENCE PAPERS ARE RELEASED!')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List the papers of the conference. IT WILL RETURN THE PAPER LIST IN THE LOCAL DATABASE')
    parser.add_argument('name', type=str, choices=['CVPR', 'ICCV', 'cvpr', 'iccv'],
                        help='Input the name of the conference')
    parser.add_argument('-p', '--period', type=int, default=1,
                        help='Input the latest \'p\' years of conference that aims to search')
    parser.add_argument('-m', '--mode', type=int, default=0, choices=[0, 1, 2],
                        help='Input the mode of the search,'
                             '0: search title, '
                             '1: search title and abstract, '
                             '2: search title and abstract and author')
    parser.add_argument('-k', '--keyword', type=str, nargs='+',
                        help='Input search keywords, using space to split words')
    return parser.parse_args()


def main():
    args = parse_args()
    name = args.name.upper()
    period = args.period
    mode = args.mode
    key_word_list = args.keyword
    if args.restore:
        init_database()
    if args.list:
        get_paper_list()
    get_paper(name, period, key_word_list, mode)


if __name__ == '__main__':
    main()
