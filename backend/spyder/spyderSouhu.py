# coding:gbk
import random
import re  # 正则表达式，进行文字匹配
import urllib.error  # 制定URL，获取网页数据
import urllib.request

import time

import requests
from bs4 import BeautifulSoup  # 网页解析，获取数据

# 创建正则表达式对象，表示规则
findlink = re.compile(' href="(.*?)"')  # 网页地址
# findbt = re.compile('原标题:(.*?)<')  #新闻标题
findrn = re.compile('/a/(.*?)_')  # 浏览量
findnr1 = re.compile('<p>(.*?)</p>')
findnr2 = re.compile('<span>(.*?)</span>')
findnr3 = re.compile('<p class="ql-align-justify">(.*?)</p>')  # 正文
findti = re.compile('>(.*?)</span>')


def getData(baseurl, a):
    print("正在获取数据")
    datalist1 = []  # 标题
    datalist2 = []  # 正文
    datalist3 = []  # 网址
    datalist4 = []  # 浏览量
    datalist5 = []
    times = 0

    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select('.list16'):
        for c in item.select('li'):
            if times < 20:
                # 三分钟以后继续发下一个

                data1 = []
                data2 = []
                data3 = []
                data4 = []
                data5 = []
                c = str(c)
                Link = findlink.findall(c)
                Link = str(Link)
                Link = Change(Link)
                Linkjs = findrn.findall(Link)  # 浏览量的js网址
                Linkjs = Change(str(Linkjs))
                if 'sohu.com' in Link:
                    continue
                else:
                    Link1 = "https://www.sohu.com" + Link
                data3.append(Link1)  # 网址获取完成
                Html = askURL(Link1)
                Soup = BeautifulSoup(Html, "html.parser")
                times += 1
                for item3 in Soup.select('h1'):
                    bt = re.sub('<.*?>', "", str(item3))
                    bt = ''.join(bt)
                    bt = bt.replace("原创", '')
                    bt = bt.replace(" ", '')
                    bt = bt.replace("\n", '')
                    data1.append(bt)  # 标题获取完成
                for item2 in Soup.select(".time"):
                    ti = findti.findall(str(item2))
                    ti = str(ti)
                    ti = ti.replace('[', '')
                    ti = ti.replace(']', '')
                    ti = ti.replace("'", '')
                    data5.append(ti)

                for item4 in Soup.select('article'):  # 正文获取
                    item4 = str(item4)
                    nr = findnr1.findall(item4)
                    if nr == "":
                        nr = findnr3.findall(item4)
                        if nr == "":
                            nr = findnr2.findall(item4)
                            if nr == "":
                                continue
                    nr1 = re.sub('<.*?>', "", str(nr))
                    nr1 = ''.join(nr1)
                    nr1 = nr1.replace('[', '')
                    nr1 = nr1.replace(']', '')
                    nr1 = nr1.replace("',", '')
                    nr1 = nr1.replace("'", '')
                    nr1 = nr1.replace("返回搜狐，查看更多", '')
                    data2.append(nr1)  # 正文获取完成

                    # 浏览量获取
                Linkjs1 = "https://v2.sohu.com/public-api/articles/" + str(Linkjs) + "/pv?callback"
                rnjs = askURL(Linkjs1)
                soupjs = BeautifulSoup(rnjs, "html.parser")
                soupjs = str(soupjs)
                soupjs = soupjs.replace('(', '')
                soupjs = soupjs.replace(')', '')
                data4.append(soupjs)  # 浏览量获取完成

                a += 1

                datalist1.append(data1)
                datalist2.append(data2)
                datalist3.append(data3)
                datalist4.append(data4)
                datalist5.append(data5)
                time.sleep(70)
                print("完成%.3d条" % a)
    print("全部完成")
    print("共保存%.3d条新闻数据" % a)
    return datalist1, datalist2, datalist3, datalist4, datalist5, a


def Change(txt):
    txt = txt.replace('[', '')
    txt = txt.replace(']', '')
    txt = txt.replace("'", '')
    txt = txt.replace(' ', '')
    return txt


# 得到指定URL的网页内容

def askURL(url):
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
    html = requests.get(url=url, headers=head, proxies=proxies).text
    return html
