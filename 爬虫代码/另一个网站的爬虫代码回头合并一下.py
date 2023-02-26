
# coding:gbk
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import requests
import multiprocessing
import random
from threading import Thread
from queue import Queue
import csv
import time



Maxnum = multiprocessing.cpu_count()
# 创建正则表达式对象，表示规则
findlink = re.compile('<a href="(.*?)">')  #网页地址
findnr = re.compile('>(.*?)</p>')#正文
findti = re.compile(r'2023(.*?)　来源')  #时间
findco = re.compile(r'https://www.163.com/dy/article/(.*?).html')  #评论页面
findcom = re.compile('"cmtCount":(.*?),')  #评论数


def main():
    data = [] #链接
    urls = geturl("https://news.163.com", data)
    a=len(urls)
    urlque = Queue()
    for i in range(a):
        url = urls[i-1]
        url = str(url).replace('[','').replace(']','').replace("'",'')
        urlque.put(url)

    csvfile = open('wy.csv', 'a', newline='', encoding='gbk')
    header = ['标题', '正文', '链接', '评论数', '时间']
    writer = csv.DictWriter(csvfile, header)
    writer.writeheader()
    for i in range(70):
        url = urlque.get()
        t1 = Thread(target=getData, args=((url, writer)))
        t1.start()


def geturl(dataurl,datalist):
    html = askURL(dataurl)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select('.hidden'):
        for c in item.select('a'):
            data = []
            Link = findlink.findall(str(c))
            Link = str(Link)
            Link = Change(Link)
            data.append(Link)
            data = Change(str(data))
            datalist.append(data)
    return datalist


def getData(url, writer):
    comm = findco.findall(url)
    if len(comm) != 0:
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")

        for item1 in soup.select('h1'):
            bt = re.sub('<.*?>', "", str(item1))
            bt = ''.join(bt)             #标题

        item2 = soup.select(".post_info")
        ti = findti.findall(str(item2))
        ti = str(ti)
        ti = ti.replace('[','').replace(']','').replace("'",'')
        ti = '2023'+ti

        item4 = soup.select('.post_body')  # 正文获取
        item4 = str(item4)
        nr = findnr.findall(item4)
        nr = re.sub('<.*?>', "", str(nr))
        nr = ''.join(nr)
        nr = nr.replace('[', '')
        nr = nr.replace(']', '')
        nr = nr.replace("',", '')
        nr = nr.replace("'", '')  # 正文获取完成

        commurl = "https://comment.tie.163.com/" + Change(str(comm)) + ".html"
        Html = askURL(commurl)
        Soup = BeautifulSoup(Html, "html.parser")
        pl = findcom.findall(str(Soup))
        pl = Change(str(pl))                #评论数
        if len(nr) != 0 and len(bt) != 0:
            writer.writerow({'标题': bt, '正文': nr, '链接': url, '评论数': pl, '时间': ti})



def Change(txt):
    txt = txt.replace('[', '')
    txt = txt.replace(']', '')
    txt = txt.replace("'", '')
    txt = txt.replace(' ', '')
    return txt

# 得到指定URL的网页内容

def askURL(url):
    # 打开文件，换行读取
    f = open("IP.txt", "r")
    file = f.readlines()
    # 遍历并分别存入列表，方便随机选取IP
    item = []
    for proxies in file:
        proxies = eval(proxies.replace('\n', ''))  # 以换行符分割，转换为dict对象
        item.append(proxies)
    proxies = random.choice(item)  # 随机选取一个IP

    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"}
    # 模拟浏览器头部信息，向服务器发送消息
    html = ""
    html = requests.get(url=url, headers=head, proxies = proxies).text
    return html


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end-start)
