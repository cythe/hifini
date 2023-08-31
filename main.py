#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import re
import requests
from lxml import etree

# ========== User config ===========

SAVE_DIRECTORY='music'
PLAYER='vlc'


# ======= Downloader Code ==========

homepage = 'https://www.hifini.com/'
headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        }


def re_find(what, where):
    obj = re.search('{}:(.*)\'(.*)\''.format(what), where)
    if obj:
        return obj.group(2)
    else:
        print("No title found.")
        return None


# e.g. https://www.hifini.com/thread-*.htm
def get_real_music_data(url):
    page = requests.get(url, headers=headers).text
    html = etree.HTML(page)
    aplayer = html.xpath("//div[@class='message break-all']/script")

    title = re_find('title', aplayer[1].text)
    author = re_find('author', aplayer[1].text)
    music_php_url = re_find('url', aplayer[1].text)

    resp = requests.get("{}{}".format(homepage, music_php_url), headers=headers)
    if resp.history:
        # get last response
        last_response = resp.history[-1]
        music_real_url = last_response.headers['location']

        music_name = '{}-{}.temp'.format(author, title)
        return music_name, music_real_url
    else:
        return 'NONE'


def download_from_music_page(music_page):
    filename, real_url = get_real_music_data(music_page)
    if real_url == 'NONE':
        print("Can't get real_url.")
        return

    print("Downloading {}...".format(filename))
    content = requests.get(real_url).content
    with open('{}/{}'.format(SAVE_DIRECTORY, filename), 'wb') as f:
        f.write(content)



def show_main():
    print("#### Hifini Music Downloader ####")
    print("1. search by name")
    print("2. search by lyric")
    print("3. download directly")
    print("4. exit")
    print()
    select = input("Command input: ")
    numbers = re.findall(r"\d+", select)
    return numbers[0]


def show_list(url):
    url = '{}{}'.format(homepage, "thread-346.htm")
    pass


def str_to_bytes(s):
    ls = []
    bytes = s.encode('utf-8')
    for b in bytes:
        ls.append(format(b, 'X'))
    return '_'.join(ls)


def show_select(t):
    if t == '1':
        s = input("Input music name: ")
        bytes = str_to_bytes(s)
        url_search = "{}search-_{}-1.htm".format(homepage, bytes)
        print(url_search)
    elif t == '2':
        s = input("Input music lyric: ")
        bytes = str_to_bytes(s)
        url_search = "{}search-_{}-0.htm".format(homepage, bytes)
        print(url_search)
    elif t == '3':
        s = input("Input music page: ")
        download_from_music_page(s)
        return 0
    elif t == '4':
        sys.exit(0)
    else:
        return 0

    return url_search


def tui():
    while True:
        select = show_main()
        search_ret = show_select(select)
        if search_ret == 0:
            continue
        else:
            print(search_ret)


if __name__ == "__main__":
    if not os.path.exists(SAVE_DIRECTORY):
        os.mkdir(SAVE_DIRECTORY)
    tui()

