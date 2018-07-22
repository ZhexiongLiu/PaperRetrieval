# PaperSpider
This project is designed to download specific CVPR, ICCV papers by retrieving keywords.

Please make sure users have installed Python3 with the packages `os`, `re`, `argparse`, `urllib` and `pandas`.

# Advance Mode:
This mode aims to download papers related to keywords inputted through parameter set using local database, which is able to retrieve keywords in titles, abstracts and authors. Users could request help using the command: *`$ python main.py -h`*.

* `-r, --restore` restores the local database in `.h5` format. PLEASE SET IT ONLY IF NEW CONFERENCE PAPERS ARE RELEASED!
* `-l, --list` lists the papers of the conference in `.html` format. IT WILL RETURN THE PAPER LIST IN THE LOCAL DATABASE.
* `name, type = str, choices = ['CVPR', 'ICCV', 'cvpr', 'iccv']` specifies the name of the conference. 
* `-p, --period, type = int, default = 1` specifies the latest `p` years of conference to retrieve.
* `-m, --mode, type = int, default = 0, choices = [0, 1, 2]` specifies the mode of the retrieving:  
`0: retrieve in the titles; 1: retrieve in the titles and abstracts; 2: retrieve in the titles and abstracts and authors`.
* `-k, --keyword, type = str` specifies a set of keywords splited by space to retrieve related papers.

## Example:
* Users could run `main.py` to download `CVPR` papers related to `deep`, `gan`, `cnn` and published within `2` years:  
*`$ python main.py CVPR -p 2 -m 1 -k deep gan cnn`*.

# Lite Mode:
This mode aims to download papers related to keywords inputted through parameter set WITHOUT using local database, which ONLY retrieves keywords in the titles. Users could request help using the command: *`get_paper_lite.py -h`*.

* `name, type = str, choices = ['CVPR', 'ICCV', 'cvpr', 'iccv']` specifies the name of the conference.
* `year, type = int` specifies the year of the conference.
* `-k, --keyword, type = str` specifies a set of keywords splited by space to retrieve related papers.

## Example:
* users could run `get_paper_lite.py` to download `CVPR 2018` papers related to `deep`, `gan`, `cnn`:  
*`$ python get_paper_lite.py CVPR 2018 -k deep gan cnn`*.
