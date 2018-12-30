"""wcount.py: count words from an Internet file.

__author__ = "He Jiawei"
__pkuid__  = "1800011753"
__email__  = "1800011753@pku.edu.cn"
"""

import sys
from urllib.request import urlopen
import urllib


def add_count(aword, adict):
    if aword not in adict.keys():
        adict[aword] = 1
    else:
        adict[aword] += 1


def wcount(lines, topn=10):
    """count words from lines of text string, then sort by their counts
    in reverse order, output the topn (word count), each in one line.
    :param lines: the file lines(or url lines), string type
    :param topn: Default 10
    """
    commas = [',', '!', '?', ':', '.', '"', "'", '_', ';', '[', ']', '(', ')']
    statistic = {}
    words = lines.split()
    # your code goes here
    for word in words:
        if word.strip() != '':
            word = word.strip()
            # check if there are any punctuation
            for comma in commas:
                while comma in word[-1]:
                    word = word[:-1]
                if comma in word[0]:
                    word = word[1:]
            if '-\n' in word:
                curr_word = (word.strip('\n')[:-1] + words[words.index(word)+1].strip()).lower()
            elif '--' in word:
                cursplit = word.split('--')
                for thing in cursplit:
                    add_count(thing, statistic)
            else:
                curr_word = word.strip().lower()

            add_count(curr_word, statistic)
    i = 1
    for key in sorted(statistic, key=statistic.__getitem__, reverse=True):
        if i <= topn:
            print(key, statistic[key], sep='\t', end='\n')
            i += 1
        else:
            break


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('Usage: {} url [topn]'.format(sys.argv[0]))
        print('  url: URL of the txt file to analyze ')
        print('  topn: words counted to output. If not given, output top 10 words')
        sys.exit(1)

    url = sys.argv[1]
    if len(sys.argv) == 2:
        topn = 10
    else:
        topn = int(sys.argv[2])
    try:
        web_file = urlopen(url)
        lines_byte = web_file.read()
        web_file.close()
        lines = bytes.decode(lines_byte)
        if topn <= 0:
            sys.stdout.write('Please Enter a positive number!')
        else:
            wcount(lines, topn)
    except urllib.request.URLError:
        sys.stdout.write('Web path unexist or denied request!')
    except ValueError:
        sys.stdout.write('Unsupported url format "{}" !'.format(url))
    #except Exception:
        #sys.stdout.write('Other unpredictable error, please ensure the url starts with "http://" and check your spelling')
