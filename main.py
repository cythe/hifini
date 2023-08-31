#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import http
import urllib.request as urlreq
import requests
import sys
from lxml import etree

# ========== User config ===========

SAVE_DIRECTORY='music'
PLAYER='vlc'


# ======= Downloader Code ==========

homepage = 'https://www.hifini.com/'
headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        }


def getpage(url):
    cookie = http.cookiejar.CookieJar()
    handler = urlreq.HTTPCookieProcessor(cookie)
    opener = urlreq.build_opener(handler)
    urlreq.install_opener(opener)
    #req = urlreq.Request(url,headers=headers,method="GET")
    req = urlreq.Request(url,headers=headers)
    res = urlreq.urlopen(req).read()
    return res


def re_find(what, where):
    obj = re.search('{}:(.*)\'(.*)\''.format(what), where)
    if obj:
        return obj.group(2)
    else:
        print("No title found.")
        return None

# e.g. https://www.hifini.com/thread-*.htm
def download(url):
    page = getpage(url).decode('utf-8')
    html = etree.HTML(page)
    #info = html.xpath("//h4[@class='break-all']")
    #print(info[0].text)
    aplayer = html.xpath("//div[@class='message break-all']/script")
    # print(aplayer[1].text)

    title = re_find('title', aplayer[1].text)
    author = re_find('author', aplayer[1].text)
    music_url = re_find('url', aplayer[1].text)

    resp = getpage("{}{}".format(homepage, music_url))
    with open('{}/{}-{}.mp3'.format(SAVE_DIRECTORY, author, title), 'wb') as f:
        f.write(resp)


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
        download(s)
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

