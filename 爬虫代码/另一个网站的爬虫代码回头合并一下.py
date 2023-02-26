
# coding:gbk
from bs4 import BeautifulSoup  # ��ҳ��������ȡ����
import re  # ������ʽ����������ƥ��
import requests
import multiprocessing
import random
from threading import Thread
from queue import Queue
import csv
import time



Maxnum = multiprocessing.cpu_count()
# ����������ʽ���󣬱�ʾ����
findlink = re.compile('<a href="(.*?)">')  #��ҳ��ַ
findnr = re.compile('>(.*?)</p>')#����
findti = re.compile(r'2023(.*?)����Դ')  #ʱ��
findco = re.compile(r'https://www.163.com/dy/article/(.*?).html')  #����ҳ��
findcom = re.compile('"cmtCount":(.*?),')  #������


def main():
    data = [] #����
    urls = geturl("https://news.163.com", data)
    a=len(urls)
    urlque = Queue()
    for i in range(a):
        url = urls[i-1]
        url = str(url).replace('[','').replace(']','').replace("'",'')
        urlque.put(url)

    csvfile = open('wy.csv', 'a', newline='', encoding='gbk')
    header = ['����', '����', '����', '������', 'ʱ��']
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
            bt = ''.join(bt)             #����

        item2 = soup.select(".post_info")
        ti = findti.findall(str(item2))
        ti = str(ti)
        ti = ti.replace('[','').replace(']','').replace("'",'')
        ti = '2023'+ti

        item4 = soup.select('.post_body')  # ���Ļ�ȡ
        item4 = str(item4)
        nr = findnr.findall(item4)
        nr = re.sub('<.*?>', "", str(nr))
        nr = ''.join(nr)
        nr = nr.replace('[', '')
        nr = nr.replace(']', '')
        nr = nr.replace("',", '')
        nr = nr.replace("'", '')  # ���Ļ�ȡ���

        commurl = "https://comment.tie.163.com/" + Change(str(comm)) + ".html"
        Html = askURL(commurl)
        Soup = BeautifulSoup(Html, "html.parser")
        pl = findcom.findall(str(Soup))
        pl = Change(str(pl))                #������
        if len(nr) != 0 and len(bt) != 0:
            writer.writerow({'����': bt, '����': nr, '����': url, '������': pl, 'ʱ��': ti})



def Change(txt):
    txt = txt.replace('[', '')
    txt = txt.replace(']', '')
    txt = txt.replace("'", '')
    txt = txt.replace(' ', '')
    return txt

# �õ�ָ��URL����ҳ����

def askURL(url):
    # ���ļ������ж�ȡ
    f = open("IP.txt", "r")
    file = f.readlines()
    # �������ֱ�����б��������ѡȡIP
    item = []
    for proxies in file:
        proxies = eval(proxies.replace('\n', ''))  # �Ի��з��ָת��Ϊdict����
        item.append(proxies)
    proxies = random.choice(item)  # ���ѡȡһ��IP

    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"}
    # ģ�������ͷ����Ϣ���������������Ϣ
    html = ""
    html = requests.get(url=url, headers=head, proxies = proxies).text
    return html


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end-start)
