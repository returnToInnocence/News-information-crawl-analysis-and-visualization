
# coding:gbk
from bs4 import BeautifulSoup  # ��ҳ��������ȡ����
import re  # ������ʽ����������ƥ��
import urllib.request,urllib.error  # �ƶ�URL����ȡ��ҳ����
import time


# ����������ʽ���󣬱�ʾ����
findlink = re.compile(' href="(.*?)"')  #��ҳ��ַ
#findbt = re.compile('ԭ����:(.*?)<')  #���ű���
findrn = re.compile('/a/(.*?)_')       #�����
findnr1 = re.compile('<p>(.*?)</p>')
findnr2 = re.compile('<span>(.*?)</span>')
findnr3 = re.compile('<p class="ql-align-justify">(.*?)</p>')  #����



def main():
    a = 1
    # ��ȡ��ҳ����ȡ����
    baseurl = "https://www.sohu.com"
    Datalist1, Datalist2, Datalist3, Datalist4, a = getData(baseurl, a)
    # ��������
    saveData(Datalist1, Datalist2, Datalist3, Datalist4, a)


def getData(baseurl, a):
    print("���ڻ�ȡ����")
    datalist1 = []  #����
    datalist2 = []  #����
    datalist3 = []  #��ַ
    datalist4 = []  #�����
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.select('.list16'):
        for c in item.select('li'):
            data1 = []
            data2 = []
            data3 = []
            data4 = []
            c = str(c)
            Link = findlink.findall(c)
            Link = str(Link)
            Link = Change(Link)
            Linkjs = findrn.findall(Link)         #�������js��ַ
            Linkjs = Change(str(Linkjs))
            if 'sohu.com' in Link:
                continue
            else:
                Link1 = "https://www.sohu.com" + Link
            data3.append(Link1)                       #��ַ��ȡ���
            Html = askURL(Link1)
            Soup = BeautifulSoup(Html, "html.parser")
            time.sleep(0.1)
            for item2 in Soup.select(".text-title"):  #�����ȡ
                for item3 in item2.select('h1'):
                    bt = re.sub('<.*?>', "", str(item3))
                    bt = ''.join(bt)
                    bt = bt.replace("ԭ��", '')
                    bt = bt.replace(" ", '')
                    bt = bt.replace("\n", '')
                    data1.append(bt)                 #�����ȡ���

            for item4 in Soup.select('article'):    #���Ļ�ȡ
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
                nr1 = nr1.replace('[','')
                nr1 = nr1.replace(']', '')
                nr1 = nr1.replace("',", '')
                nr1 = nr1.replace("'", '')
                nr1 = nr1.replace("�����Ѻ����鿴����", '')
                data2.append(nr1)                  #���Ļ�ȡ���

                                                     #�������ȡ
            Linkjs1 = "https://v2.sohu.com/public-api/articles/" + str(Linkjs) + "/pv?callback"
            rnjs = askURL(Linkjs1)
            soupjs = BeautifulSoup(rnjs,"html.parser")
            soupjs = str(soupjs)
            soupjs = soupjs.replace('(','')
            soupjs = soupjs.replace(')','')
            data4.append(soupjs)                     #�������ȡ���

            a += 1

            datalist1.append(data1)
            datalist2.append(data2)
            datalist3.append(data3)
            datalist4.append(data4)
    print("������%.3d����������" % a)
    return datalist1, datalist2, datalist3, datalist4, a


def saveData(Datalist1, Datalist2, Datalist3, Datalist4, a):
    with open('sohu����.txt', 'a+',encoding='utf-8') as f:
        for i in range(1, a):
            aa = ''.join('%s' % a for a in Datalist1[i - 1])
            bb = ''.join('%s' % a for a in Datalist2[i - 1])
            cc = ''.join('%s' % a for a in Datalist3[i - 1])
            dd = ''.join('%s' % a for a in Datalist4[i - 1])
            k = ''
            if aa == '' or bb == '':
                continue
            f.write(aa)
            f.write("\n")
            f.write(bb)
            f.write("\n")
            f.write(cc)
            f.write("\n")
            f.write(dd)
            f.write("\n --------- \n")
    print("�������")


def Change(txt):
    txt = txt.replace('[', '')
    txt = txt.replace(']', '')
    txt = txt.replace("'", '')
    txt = txt.replace(' ', '')
    return txt

# �õ�ָ��URL����ҳ����

def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"}
    # ģ�������ͷ����Ϣ���������������Ϣ
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8", 'ignore')
        response.close()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":
    main()
