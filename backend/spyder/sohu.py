import requests
from bs4 import BeautifulSoup
import lxml
import re
import json
from jieba import analyse
import pymysql


class SouhuSpider:
    # �Ѻ���վ��ȡ���������İ�����ݣ��������֡��ƾ����������������Ƽ�
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'
    }
    date = '2023-1-18'

    def __init__(self):
        self.souhu_author_data_list = []  # �������ֺ�����
        # �Ѻ������б�
        self.souhu_article = []
        # �Ѻ��ؼ����б�
        self.souhu_key1 = []
        self.souhu_key = []
        # �Ѻ������б�
        self.souhu_author = []
    @staticmethod
    def souhu_plate1(text):
        ex1 = r'<div class="main left">(.*?)<div class="sidebar right">'
        ex_article = r'<div class="main-right right" data-role="main-news">(.*?)<div class="main-box.*?>'
        five_ex1 = re.findall(ex1, text, re.S | re.M)  # ����ƥ���ϵ������飺���֡��������ƾ����������Ƽ���
        five_ex_article = re.findall(ex_article, text, re.S | re.M)
        article_list = []
        href_total = []
        plate1 = []
        plate_a = []
        h = 0
        for article_plate in five_ex_article:
            ex1_a = r'<li>.*?<a.*?>(.*?)</a>'
            ex1_a_href = r'<li>.*?<a.*?href="(.*?)".*?>.*?</a>'  # ��������
            list_article = re.findall(ex1_a, article_plate, re.M | re.S)
            list_article_href = re.findall(ex1_a_href, article_plate, re.M | re.S)
            h = h + 1
            for x in range(len(list_article_href)):
                if (h == 1 or h == 3 or h == 5):
                    if (list_article_href[x].find('http') == -1):
                        list_article_href[x] = 'https://www.sohu.com' + list_article_href[x]
                else:
                    if (list_article_href[x].find('http') == -1):
                        list_article_href[x] = 'https:' + list_article_href[x]
            href_total.append(list_article_href)
            for j in range(len(list_article)):
                list_article[j] = list_article[j].replace('<strong>', '')
                list_article[j] = list_article[j].replace('</strong>', '')
                list_article[j] = list_article[j].replace('\n', '')
                list_article[j] = list_article[j].replace(' ', '')
            article_list.append(list_article)
        # print(href_total)     #��������
        # print(article_list)  #������Ŀ
        art_hrftotal = []
        for y in range(len(article_list)):
            artsmall_hrftotal = []
            for z in range(len(article_list[y])):
                art_hre = (article_list[y][z], href_total[y][z])
                artsmall_hrftotal.append(art_hre)
            art_hrftotal.append(artsmall_hrftotal)
        # print(art_hrftotal)   #�������Ӻͱ��⣨���⣬���ӣ�
        ul_list = []  # ul_list�洢���������ul��ǩ
        li_list1 = []  # ul_list�洢���������li��ǩ
        for text_plate in five_ex1:
            ex1 = r'<ul>.*?</ul>'
            list = re.findall(ex1, text_plate, re.M | re.S)
            list_text = list[0]
            ul_list.append(list_text)
        for li_list in ul_list:
            small_plate = ''
            li = []
            ex2 = r'<li.*?>.*?<a href=".*?>(.*?)</a>'  # ��ȡ�İ������
            ex3 = r'<li.*?>.*?<a href="(.*?)" .*?>.*?</a>'  # ��ȡ�İ������
            list_li = re.findall(ex2, li_list, re.M | re.S)
            list_href = re.findall(ex3, li_list, re.M | re.S)
            for j in range(len(list_li)):
                list_1 = list_li[j].replace('\n', '')
                list_2 = list_1.replace(' ', '')
                list_3 = (list_2, list_href[j])
                li.append(list_3)
            if li != []:
                li_list1.append(li)
            if len(li) == 1:
                small_plate = '��'
            for p in range(1, len(li)):
                if p != (len(li) - 1):
                    small_plate = small_plate + li[p][0] + '/'
                else:
                    small_plate = small_plate + li[p][0]
            try:
                plate1 = [li[0][0], 0, li[0][1], small_plate]
            except IndexError:
                break
            else:
                plate1 = [li[0][0], 0, li[0][1], small_plate]
                plate_a.append(plate1)
            # print(plate1)
        list_article_total = []
        for i in range(len(li_list1)):
            list_article_total1 = []
            list_article_total1.append(li_list1[i][0][0])
            list_article_total1 = list_article_total1 + art_hrftotal[i]
            list_article_total.append(list_article_total1)
        # for i in range(5):
        #     print(list_article_total[i])
        # print(len(list_article_total))
        # print(list_article_total)
        return (li_list1, list_article_total, plate_a)

    # �Ѻ���վ��ȡСƵ������İ�����ݣ�������������ʷ�������������Ϸ
    def souhu_plate2(self, text):
        soup1 = BeautifulSoup(text, 'lxml')
        text_other = soup1.find_all("div", class_="area clearfix public content-other")  # ȡ����СƵ������Դ����
        text_other = str(text_other[0])  # ת��Ϊstr����
        soup2 = BeautifulSoup(text_other, 'lxml')
        text_left = soup2.find_all("div", class_="main left")
        text_left = str(text_left[0])  # main-left���
        soup3 = BeautifulSoup(text_left, 'lxml')
        text_plate = soup3.find_all("div", class_="main-box")  # ����߸��Ӱ��
        li_list2 = []
        li_s = []
        lists_article = []
        lists_article_href = []
        lists_article_total = []
        plate2 = []
        plate_b = []
        for plate in text_plate:
            soup4 = BeautifulSoup(str(plate), 'lxml')
            text_li = soup4.find_all("span", class_="tt")  # ������
            text_article = soup4.find_all("div", class_="list16")
            for li_article in text_article:
                ex1_a = r'<li>.*?<a.*?href=".*?".*?>(.*?)</a>'  # ��ȡ���±���
                ex1_ah = r'<li>.*?<a.*?href="(.*?)".*?>.*?</a>'  # ��ȡ��������
                lif = re.findall(ex1_a, str(li_article), re.M | re.S)
                lia = re.findall(ex1_ah, str(li_article), re.M | re.S)
                for x in range(len(lia)):
                    lia[x] = 'https://www.sohu.com' + lia[x]
                lists_article_href.append(lia)
                for j in range(len(lif)):
                    lif[j] = lif[j].replace('<strong>', '')
                    lif[j] = lif[j].replace('</strong>', '')
                    lif[j] = lif[j].replace('\n', '')
                    lif[j] = lif[j].replace(' ', '')
                lists_article.append(lif)
            for li in text_li:
                li1 = []
                soup5 = BeautifulSoup(str(li), 'lxml')
                li1_total = (str(soup5.span.string), 'https:' + str(soup5.span.a['href']))
                li1.append(li1_total)
                li_list2.append(li1)  # ������б�
            soup6 = BeautifulSoup(str(plate), 'lxml')
            text_lis = soup6.find_all("span", class_="link")  # ÿ�������Ӱ��
            for lis in text_lis:
                soup7 = BeautifulSoup(str(lis), 'lxml')
                li2_total = (str(soup7.span.string), str(soup7.span.a['href']))
                li_s.append(li2_total)
        # print(lists_article_href)
        for i in range(0, len(li_list2)):
            for j in range(0, len(li_s)):
                if (j // 3 == i):
                    li_list2[i].append(li_s[j])

        for p in range(0, len(li_list2)):
            small_plate = ''
            for q in range(1, len(li_list2[p])):
                if (q != 3):
                    small_plate = small_plate + li_list2[p][q][0] + '/'
                else:
                    small_plate = small_plate + li_list2[p][q][0]
            plate2 = [li_list2[p][0][0], 0, li_list2[p][0][1], small_plate]
            plate_b.append(plate2)
        # print(lists_article) #������Ŀ
        art_hrftotal = []
        for y in range(len(lists_article)):
            artsmall_hrftotal = []
            for z in range(len(lists_article[y])):
                art_hre = (lists_article[y][z], lists_article_href[y][z])
                artsmall_hrftotal.append(art_hre)
            art_hrftotal.append(artsmall_hrftotal)
        # print(art_hrftotal)
        for i in range(len(li_list2)):
            list_article_total1 = []
            list_article_total1.append(li_list2[i][0][0])
            list_article_total1 = list_article_total1 + art_hrftotal[i]
            lists_article_total.append(list_article_total1)
        # for i in range(14):
        #     print(lists_article_total[i]) #����������Ͱ������º�����
        return (li_list2, lists_article_total, plate_b)

    # �Ѻ���վ��ȡ����������
    def souhu_article_comment(self, href):
        url = href
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
        }
        article_html = requests.get(url=url, headers=headers).text
        ex1 = r"newsId : '(.*?)'"
        newsId = re.findall(ex1, article_html, re.M | re.S)
        newId = newsId[0]
        href_comment = 'https://uis.mp.sohu.com/wap/api/comments?sourceId=mp_' + newId + '&pageNo=1&pageSize=10&type=0'
        comment_json = requests.get(url=href_comment, headers=headers).text
        ex2 = r"participation.*?:(.*?),"
        comment = re.findall(ex2, comment_json, re.M | re.S)
        comment = comment[0]
        # print(comment)
        # print(newId)
        return comment

    # �Ѻ�����ȡ���µ���Ϣ�����ߡ������������ؼ��ֵ�
    def souhu_article_table(self, type, title, href):
        url = href
        if url.find('tv.sohu.com') != -1:
            return
        else:
            article_html = requests.get(url=url, headers=self.headers).text
            soup = BeautifulSoup(article_html, 'lxml')
            text_article = soup.select('#article-container')  # ��box
            soup1 = BeautifulSoup(str(text_article), 'lxml')
            text_article1 = soup1.select('.column')
            soup2 = BeautifulSoup(str(text_article1), 'lxml')
            global author_data_list
            try:
                soup2.h4.a.string
            except AttributeError:
                return
            else:
                author = soup2.h4.a.string  # ��������
                author_href = soup.h4.a['href']
                # author_data = (author, author_href)
                # # print(author_data)
                # if(souhu_author_data_list.count(author_data) == 0):
                #     souhu_author_data_list.append(author_data)
            # print(author)
            comment = self.souhu_article_comment(href)
            # print(comment)                 #����
            text_time = soup1.select('.article-info')
            soup4 = BeautifulSoup(str(text_time), 'lxml')
            time = soup4.span.string  # ʱ��
            # print(time)
            patten1 = re.compile(
                '(2.*?) ')
            results = re.findall(patten1, time)
            # print(results)
            if results is not None:
                time = results[0]
            else:
                time = self.date
            text_address = soup1.find_all("div", class_="text")
            ex1 = r'<div class="area"><span>.*?</span><span>(.*?)</span>'
            address = re.findall(ex1, str(text_address), re.S | re.M)
            # print(address[0])                         #��ַ
            try:
                author_data = (author, author_href, address[0])
            except IndexError:
                author_data = (author, author_href, '��')
            else:
                author_data = (author, author_href, address[0])
                if self.souhu_author_data_list.count(author_data) == 0:
                    self.souhu_author_data_list.append(author_data)
                # print(author_data)
            text_word = soup1.select('.article')  # ��������div
            soup5 = BeautifulSoup(str(text_word), 'lxml')
            word = soup5.p.text
            word = word.replace(' ', '')
            word = word.replace('\n', '')
            # print(word)                             #����
            length = len(word)  # ����
            # print(length)
            keywords = analyse.extract_tags(word, topK=1, withWeight=False)
            keyword = keywords[0]  # �ؼ���
            # print(keyword)
            amount = word.count(keyword)  # �ؼ��ֳ��ִ���
            # print(amount)
            try:
                total = (title, author, '�Ѻ�', length, type, comment, time, keyword, amount, address[0])
            except IndexError:
                return
            else:
                # cursor = conn.cursor()
                # # ʹ�� execute()  ����ִ�� SQL ��ѯ
                # cursor.execute("show databases;")
                # cursor.execute("use `database`;")
                # source = '�Ѻ�'
                # comment_count = 8
                # sql = """insert into `essay`(`id`,`title`,`author`,`source`,`word_count`,`type`,`comment_count`,`publish_time`,`keyword`,`keyword_count`,`publish_address`,`article_link`) values ('%d','%s','%s','%s','%d','%s','%d','%s','%s','%d','%s','%s')"""%(id, title, author, source, length, type, comment_count, time, keyword, amount, address[0],href)
                # try:
                #     # ִ��sql���
                #     cursor.execute(sql)
                #     # �ύ�����ݿ�ִ��
                #     conn.commit()
                #     cursor.close()
                # except:
                #     # Rollback in case there is any error
                #     conn.rollback()
                total = [title, author, '�Ѻ�', length, type, comment, time, keyword, amount, address[0], href]
                self.souhu_article.append(total)
                # print(total)

    # �Ѻ�����ȡ������Ϣ���������ͷ�˿������顢������
    def souhu_author_information(self, name, href, address):
        url = href
        author_html = requests.get(url=url, headers=self.headers).text
        soup = BeautifulSoup(author_html, 'lxml')
        text_author = soup.select('.main')  # ��box
        soup1 = BeautifulSoup(str(text_author), 'lxml')
        text_box = soup.select('#block4')
        ex1 = 'renderData:(.*?)</script>'
        author_data = re.findall(ex1, str(text_box), re.S | re.M)
        ex2 = r'''"column_15_text":(.*?),'''
        try:
            fans = re.findall(ex2, author_data[0], re.S | re.M)
        except IndexError:
            return
        else:
            fans = fans[0]  # ����������˿��
        # print(fans)
        ex3 = r'''"column_5_text":(.*?),'''
        article_count = re.findall(ex3, author_data[0], re.S | re.M)
        article_count = article_count[0]  # ������
        # print(article_count)
        ex4 = r'''"id":"(.*?)"'''
        id = re.findall(ex4, author_data[0], re.S | re.M)
        id = id[0]  # id
        # print(id)
        ex5 = r'''"column_9_text":"(.*?)"'''  # ���
        introduce = re.findall(ex5, author_data[0], re.S | re.M)
        try:
            introduce1 = introduce[0]
        except IndexError:
            introduce1 = 'None'
        else:
            introduce1 = introduce[0]
        # print(introduce)
        source = "�Ѻ�"
        total = [name, article_count, address, introduce1, fans, source]
        self.souhu_author.append(total)
        # print(total)

    def run(self):
        # #�������ݿ�
        # conn = pymysql.connect(host='localhost',
        #                        port=3306,
        #                        user='root',
        #                        passwd='',
        #                        db='database',
        #                        charset='utf8',
        #                        cursorclass=pymysql.cursors.DictCursor
        #                        )
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'
        # }
        #

        url_sohu = 'https://www.sohu.com/'
        # ʹ��ͨ�������url��Ӧ��һ����ҳ�������ȡ
        souhu_page_text = requests.get(url=url_sohu, headers=self.headers).text
        souhu_soup = BeautifulSoup(souhu_page_text, 'lxml')
        souhu_text_wrapper = souhu_soup.select('.wrapper-box')  # ����������
        souhu_text = str(souhu_text_wrapper[0])
        souhu_li_all = []  # ��������
        souhu_li_article = []  # ����������Ŀ
        # ����б�
        souhu_plate = []
        souhu_li_all = self.souhu_plate1(souhu_text)[0] + self.souhu_plate2(souhu_text)[0]
        souhu_li_article = self.souhu_plate1(souhu_text)[1] + self.souhu_plate2(souhu_text)[1]
        souhu_plate = self.souhu_plate1(souhu_text)[2] + self.souhu_plate2(souhu_text)[2]
        print(souhu_plate)
        for k in range(len(souhu_li_article)):
            for a in range(1, len(souhu_li_article[k])):
                type = souhu_li_article[k][0]
                title = souhu_li_article[k][a][0]
                href = souhu_li_article[k][a][1]
                menu = (type, title, href)
                self.souhu_article_table(type, title, href)
        for s in self.souhu_author_data_list:
            # print(s)  # �������ֺ�����
            self.souhu_author_information(s[0], s[1], s[2])
        print(self.souhu_author)
        print(self.souhu_article)
        for l in range(0, len(self.souhu_article)):
            if self.souhu_key1.count(self.souhu_article[l][7]) == 0:
                self.souhu_key1.append(self.souhu_article[l][7])
        for m in self.souhu_key1:
            middle = []
            middle = [m, 0, 0]
            self.souhu_key.append(middle)
        print(self.souhu_key)
        print(self.souhu_key1)
        return souhu_plate, self.souhu_key, self.souhu_author, self.souhu_article


if __name__ == '__main__':
    w = SouhuSpider()
    a, b, c, d = w.run()
    print(a)
    print(b)
    print(c)
    print(d)
