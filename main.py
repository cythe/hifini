#!/usr/bin/python
# -*- coding:utf-8 -*-

# 导入外部依赖
import re
import http
import urllib.request as urlreq
import requests
import signal
import sys
from lxml import etree

headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        }

# ========== 下载器实现 ============
# 导入requests 库
import requests
# 导入 tqdm
from tqdm import tqdm
#def download(url: str, file_name: str):
#    # 文件下载直链
#    # 请求头
#    # 发起 head 请求，即只会获取响应头部信息
#    head = requests.head(url, headers=headers)
#    # 文件大小，以 B 为单位
#    file_size = head.headers.get('Content-Length')
#    if file_size is not None:
#        file_size = int(file_size)
#        response = requests.get(url, headers=headers, stream=True)

def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError
        
        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError as e:
                callback()

        return to_do

    return wrap


# 1. 构建搜索URL

text = "一生所爱"
bytes = text.encode('utf-8')
print(bytes)

ls = []
for b in bytes:
    ls.append(format(b, 'X'))

print(ls)

url_search_title = "www.hifini.com/search-_{}-1.htm".format('_'.join(ls))
print(url_search_title)
url_search_context = "www.hifini.com/search-_{}-0.htm".format('_'.join(ls))
print(url_search_context)

# 2. 列出搜索内容


# 3. 对某个网页进行操作， 解析内容， 保存mp3, 记得重命名
def after_timeout():
    print("timeout!!")
    sys.exit(2)

@set_timeout(30, after_timeout)
def getpage(url):
    #s=time.time()
    cookie = http.cookiejar.CookieJar()
    handler = urlreq.HTTPCookieProcessor(cookie)
    opener = urlreq.build_opener(handler)
    urlreq.install_opener(opener)
    #req = urlreq.Request(url,headers=headers,method="GET")
    req = urlreq.Request(url,headers=headers)
    res = urlreq.urlopen(req).read()
    #e=time.time()
    #print_flushed("getpage: {}\n".format(e-s))
    return res

url = "https://www.hifini.com/thread-346.htm"

def re_find(what, where):
    obj = re.search('{}:(.*)\'(.*)\''.format(what), where) 
    if obj:
        return obj.group(2)
    else:
        print("No title found.")
        return None

def download(url):
    page = getpage(url).decode('utf-8')
    html = etree.HTML(page)
    #info = html.xpath("//h4[@class='break-all']")
    #print(info[0].text)
    aplayer = html.xpath("//div[@class='message break-all']/script")
    print(aplayer[1].text)
    
    title = re_find('title', aplayer[1].text)
    author = re_find('author', aplayer[1].text) 
    music_url = re_find('url', aplayer[1].text)
    
    resp = getpage("https://www.hifini.com/{}".format(music_url))
    with open('{}-{}.mp3'.format(author, title), 'wb') as f:
        # 写入分块文件
            f.write(resp)

download(url)

# if __name__ == "__main__":
#       main()
#
#
#
