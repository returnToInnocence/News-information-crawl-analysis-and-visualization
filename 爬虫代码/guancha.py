
# coding:gbk
from bs4 import BeautifulSoup  # ��ҳ��������ȡ����
import re  # ������ʽ����������ƥ��
import urllib.request,urllib.error  # �ƶ�URL����ȡ��ҳ����
import requests
import multiprocessing
import random
from threading import Thread
from queue import Queue
import csv
import time



Maxnum = multiprocessing.cpu_count()
# ����������ʽ���󣬱�ʾ����
findlink = re.compile(' href="(.*?)"')  #��ҳ��ַ
#findbt = re.compile('ԭ����:(.*?)<')  #���ű���
findrn = re.compile('/a/(.*?)_')       #�����
findnr1 = re.compile('<p>(.*?)</p>')
findnr2 = re.compile('<span>(.*?)</span>')
findnr3 = re.compile('<p class="ql-align-justify">(.*?)</p>')  #����
findti = re.compile('>(.*?)</span>')


def main():
    data = [] #����
    urls = geturl("https://www.sohu.com", data)
    a=len(urls)
    urlque = Queue()
    for i in range(a):
        url = urls[i-1]
        url = str(url).replace('[','').replace(']','').replace("'",'')
        urlque.put(url)

    csvfile = open('demo.csv', 'a', newline='', encoding='gbk')
    header = ['����', '����', '����', '�Ķ���', 'ʱ��']
    writer = csv.DictWriter(csvfile, header)
    writer.writeheader()
    for i in range(a):
        url = urlque.get()
        t1 = Thread(target=getData, args=((url, writer)))
        t1.start()



def geturl(dataurl,datalist):
    times = 0
    html = askURL(dataurl)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select('.list16'):
        if times < 50:
            for c in item.select('li'):
                data = []
                Link = findlink.findall(str(c))
                Link = str(Link)
                Link = Change(Link)
                if 'sohu.com' in Link or Link == '':
                    continue
                else:
                    Link1 = "https://www.sohu.com" + Link

                data.append(Link1)
                data = Change(str(data))
                datalist.append(data)
    return datalist


def getData(url, writer):
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    Linkjs = findrn.findall(url)  # �������js��ַ
    Linkjs = Change(str(Linkjs))

    for item1 in soup.select('h1'):
        bt = re.sub('<.*?>', "", str(item1))
        bt = ''.join(bt)
        bt = bt.replace("ԭ��", '').replace(" ", '').replace("\n", '') # �����ȡ���
    item2 = soup.select(".time")
    ti = findti.findall(str(item2))
    ti = str(ti)
    ti = ti.replace('[', '')
    ti = ti.replace(']', '')
    ti = ti.replace("'", '') #����ʱ���ȡ���

    item4 = soup.select('article')  # ���Ļ�ȡ
    item4 = str(item4)
    nr = findnr1.findall(item4)
    if nr == "":
        nr = findnr3.findall(item4)
        if nr == "":
            nr = findnr2.findall(item4)
    nr1 = re.sub('<.*?>', "", str(nr))
    nr1 = ''.join(nr1)
    nr1 = nr1.replace('[', '')
    nr1 = nr1.replace(']', '')
    nr1 = nr1.replace("',", '')
    nr1 = nr1.replace("'", '')
    nr1 = nr1.replace("�����Ѻ����鿴����", '') # ���Ļ�ȡ���

        # �������ȡ
    Linkjs1 = "https://v2.sohu.com/public-api/articles/" + str(Linkjs) + "/pv?callback"
    rnjs = askURL(Linkjs1)
    soupjs = BeautifulSoup(rnjs, "html.parser")
    soupjs = str(soupjs)
    soupjs = soupjs.replace('(', '').replace(')', '') # �������ȡ���
    if len(nr1) != 0 and len(bt) != 0:
        writer.writerow({'����': bt, '����': nr1, '����': url, '�Ķ���': soupjs, 'ʱ��': ti})


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
    # start = time.time()
    main()
    # end = time.time()
    # print(end-start)
