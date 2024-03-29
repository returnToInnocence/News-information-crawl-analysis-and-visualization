# coding=gbk
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request,urllib.error  # 制定URL，获取网页数据
import requests
import multiprocessing
import random
from threading import Thread
from queue import Queue
import csv


Maxnum = multiprocessing.cpu_count()
# 创建正则表达式对象，表示规则
findlink = re.compile(' href="(.*?)"')  #网页地址
#findbt = re.compile('原标题:(.*?)<')  #新闻标题
findrn = re.compile('/a/(.*?)_')       #浏览量
findnr1 = re.compile('<p>(.*?)</p>')
findnr2 = re.compile('<span>(.*?)</span>')
findnr3 = re.compile('<p class="ql-align-justify">(.*?)</p>')  #正文
findti = re.compile('>(.*?)</span>')




ipList = [
    "{'HTTP': '27.42.168.46:55481'}\n",
    "{'HTTP': '121.13.252.61:41564'}\n",
    "{'HTTP': '202.109.157.63:9000'}\n",
    "{'HTTP': '121.13.252.62:41564'}\n",
    "{'HTTP': '121.13.252.60:41564'}\n",
    "{'HTTP': '210.5.10.87:53281'}\n",
    "{'HTTP': '183.236.232.160:8080'}\n",
    "{'HTTP': '117.114.149.66:55443'}\n",
    "{'HTTP': '222.74.73.202:42055'}\n",
    "{'HTTP': '117.93.180.62:9000'}\n",
    "{'HTTP': '27.42.168.46:55481'}\n",
    "{'HTTP': '61.216.185.88:60808'}\n",
    "{'HTTP': '61.216.156.222:60808'}\n",
    "{'HTTP': '182.34.102.50:9999'}\n",
    "{'HTTP': '210.5.10.87:53281'}\n",
    "{'HTTP': '183.236.232.160:8080'}\n",
    "{'HTTP': '117.41.38.19:9000'}\n",
    "{'HTTP': '112.14.47.6:52024'}\n",
    "{'HTTP': '222.74.73.202:42055'}\n",
    "{'HTTP': '116.9.163.205:58080'}\n",
    "{'HTTP': '202.109.157.66:9000'}\n",
    "{'HTTP': '27.42.168.46:55481'}\n",
    "{'HTTP': '121.13.252.61:41564'}\n",
    "{'HTTP': '121.13.252.58:41564'}\n",
    "{'HTTP': '182.34.102.50:9999'}\n",
    "{'HTTP': '121.13.252.60:41564'}\n",
    "{'HTTP': '210.5.10.87:53281'}\n",
    "{'HTTP': '183.236.232.160:8080'}\n",
    "{'HTTP': '121.13.252.62:41564'}\n",
    "{'HTTP': '117.41.38.19:9000'}\n",
    "{'HTTP': '112.14.47.6:52024'}\n",
    "{'HTTP': '116.9.163.205:58080'}\n",
    "{'HTTP': '202.109.157.66:9000'}\n",
    "{'HTTP': '27.42.168.46:55481'}\n",
    "{'HTTP': '61.216.185.88:60808'}\n",
    "{'HTTP': '61.216.156.222:60808'}\n",
    "{'HTTP': '202.109.157.63:9000'}\n",
    "{'HTTP': '121.13.252.60:41564'}\n",
    "{'HTTP': '210.5.10.87:53281'}\n",
    "{'HTTP': '183.236.232.160:8080'}\n",
    "{'HTTP': '121.13.252.62:41564'}\n",
    "{'HTTP': '112.14.47.6:52024'}\n"
]



# def main():
#     data = [] #链接
#     urls = geturl("https://www.sohu.com", data)
#     a=len(urls)
#     urlque = Queue()
#     for i in range(a):
#         url = urls[i-1]
#         url = str(url).replace('[','').replace(']','').replace("'",'')
#         urlque.put(url)
#     print(urlque)
#
#     csvfile = open('demo.csv', 'a', newline='', encoding='utf-8')
#     header = ['标题', '正文', '链接', '阅读量', '时间']
#     writer = csv.DictWriter(csvfile, header)
#     writer.writeheader()
#     for i in range(a):
#         url = urlque.get()
#         t1 = Thread(target=getData, args=((url, writer)))
#         t1.start()

# def main():
#     data = [] #链接
#     urls = geturl("https://www.sohu.com", data)
#     a=len(urls)
#     urlque = Queue()
#     for i in range(a):
#         url = urls[i-1]
#         url = str(url).replace('[','').replace(']','').replace("'",'')
#         urlque.put(url)
#     print(urlque)
#
#     for i in range(a):
#         url = urlque.get()
#         t1 = Thread(target=getData, args=(url,))
#         t1.start()


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

#
# def getData(url):
#     html = askURL(url)
#     soup = BeautifulSoup(html, "html.parser")
#     Linkjs = findrn.findall(url)  # 浏览量的js网址
#     Linkjs = Change(str(Linkjs))
#     bt = ""
#     for item1 in soup.select('h1'):
#         bt = re.sub('<.*?>', "", str(item1))
#         bt = ''.join(bt)
#         bt = bt.replace("原创", '').replace(" ", '').replace("\n", '') # 标题获取完成
#     item2 = soup.select(".time")
#     ti = findti.findall(str(item2))
#     ti = str(ti)
#     ti = ti.replace('[', '')
#     ti = ti.replace(']', '')
#     ti = ti.replace("'", '') #发布时间获取完成
#
#     item4 = soup.select('article')  # 正文获取
#     item4 = str(item4)
#     nr = findnr1.findall(item4)
#     if nr == "":
#         nr = findnr3.findall(item4)
#         if nr == "":
#             nr = findnr2.findall(item4)
#     nr1 = re.sub('<.*?>', "", str(nr))
#     nr1 = ''.join(nr1)
#     nr1 = nr1.replace('[', '')
#     nr1 = nr1.replace(']', '')
#     nr1 = nr1.replace("',", '')
#     nr1 = nr1.replace("'", '')
#     nr1 = nr1.replace("返回搜狐，查看更多", '') # 正文获取完成
#
#         # 浏览量获取
#     Linkjs1 = "https://v2.sohu.com/public-api/articles/" + str(Linkjs) + "/pv?callback"
#     rnjs = askURL(Linkjs1)
#     soupjs = BeautifulSoup(rnjs, "html.parser")
#     soupjs = str(soupjs)
#     soupjs = soupjs.replace('(', '').replace(')', '') # 浏览量获取完成
#     if len(nr1) != 0 and len(bt) != 0:
#         a = {'标题': bt, '正文': nr1, '链接': url, '阅读量': soupjs, '时间': ti}
#         print(a)


def Change(txt):
    txt = txt.replace('[', '')
    txt = txt.replace(']', '')
    txt = txt.replace("'", '')
    txt = txt.replace(' ', '')
    return txt

# 得到指定URL的网页内容

def askURL(url):
    # 遍历并分别存入列表，方便随机选取IP
    item = []
    for proxies in ipList:
        proxies = eval(proxies.replace('\n', ''))  # 以换行符分割，转换为dict对象
        item.append(proxies)
    proxies = random.choice(item)  # 随机选取一个IP

    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"}
    # 模拟浏览器头部信息，向服务器发送消息
    html = ""
    html = requests.get(url=url, headers=head, proxies = proxies).text
    return html

#
# if __name__ == "__main__":
#     main()

