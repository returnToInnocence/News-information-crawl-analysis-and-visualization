import requests
from bs4 import BeautifulSoup
import lxml
import re
import json
from jieba import analyse
import pymysql


class SouhuSpider:
    # 搜狐网站爬取五个规则板块的板块内容，例如娱乐、财经、体育、汽车、科技
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'
    }
    date = '2023-1-18'

    def __init__(self):
        self.souhu_author_data_list = []  # 作者名字和链接
        # 搜狐文章列表
        self.souhu_article = []
        # 搜狐关键字列表
        self.souhu_key1 = []
        self.souhu_key = []
        # 搜狐作者列表
        self.souhu_author = []
    @staticmethod
    def souhu_plate1(text):
        ex1 = r'<div class="main left">(.*?)<div class="sidebar right">'
        ex_article = r'<div class="main-right right" data-role="main-news">(.*?)<div class="main-box.*?>'
        five_ex1 = re.findall(ex1, text, re.S | re.M)  # 可以匹配上的五个板块：娱乐、体育、财经、汽车、科技。
        five_ex_article = re.findall(ex_article, text, re.S | re.M)
        article_list = []
        href_total = []
        plate1 = []
        plate_a = []
        h = 0
        for article_plate in five_ex_article:
            ex1_a = r'<li>.*?<a.*?>(.*?)</a>'
            ex1_a_href = r'<li>.*?<a.*?href="(.*?)".*?>.*?</a>'  # 文章链接
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
        # print(href_total)     #文章链接
        # print(article_list)  #文章题目
        art_hrftotal = []
        for y in range(len(article_list)):
            artsmall_hrftotal = []
            for z in range(len(article_list[y])):
                art_hre = (article_list[y][z], href_total[y][z])
                artsmall_hrftotal.append(art_hre)
            art_hrftotal.append(artsmall_hrftotal)
        # print(art_hrftotal)   #文章链接和标题（标题，链接）
        ul_list = []  # ul_list存储了五个板块的ul标签
        li_list1 = []  # ul_list存储了五个板块的li标签
        for text_plate in five_ex1:
            ex1 = r'<ul>.*?</ul>'
            list = re.findall(ex1, text_plate, re.M | re.S)
            list_text = list[0]
            ul_list.append(list_text)
        for li_list in ul_list:
            small_plate = ''
            li = []
            ex2 = r'<li.*?>.*?<a href=".*?>(.*?)</a>'  # 爬取的板块名称
            ex3 = r'<li.*?>.*?<a href="(.*?)" .*?>.*?</a>'  # 爬取的板块链接
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
                small_plate = '无'
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

    # 搜狐网站爬取小频道区块的板块内容，比如星座、历史、宠物、动漫、游戏
    def souhu_plate2(self, text):
        soup1 = BeautifulSoup(text, 'lxml')
        text_other = soup1.find_all("div", class_="area clearfix public content-other")  # 取到了小频道板块的源代码
        text_other = str(text_other[0])  # 转换为str类型
        soup2 = BeautifulSoup(text_other, 'lxml')
        text_left = soup2.find_all("div", class_="main left")
        text_left = str(text_left[0])  # main-left板块
        soup3 = BeautifulSoup(text_left, 'lxml')
        text_plate = soup3.find_all("div", class_="main-box")  # 获得七个子版块
        li_list2 = []
        li_s = []
        lists_article = []
        lists_article_href = []
        lists_article_total = []
        plate2 = []
        plate_b = []
        for plate in text_plate:
            soup4 = BeautifulSoup(str(plate), 'lxml')
            text_li = soup4.find_all("span", class_="tt")  # 板块标题
            text_article = soup4.find_all("div", class_="list16")
            for li_article in text_article:
                ex1_a = r'<li>.*?<a.*?href=".*?".*?>(.*?)</a>'  # 爬取文章标题
                ex1_ah = r'<li>.*?<a.*?href="(.*?)".*?>.*?</a>'  # 爬取文章链接
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
                li_list2.append(li1)  # 主板块列表
            soup6 = BeautifulSoup(str(plate), 'lxml')
            text_lis = soup6.find_all("span", class_="link")  # 每个板块的子板块
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
        # print(lists_article) #文章题目
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
        #     print(lists_article_total[i]) #输出各个类型板块的文章和链接
        return (li_list2, lists_article_total, plate_b)

    # 搜狐网站爬取文章评论数
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

    # 搜狐网爬取文章的信息，作者、文章字数、关键字等
    def souhu_article_table(self, type, title, href):
        url = href
        if url.find('tv.sohu.com') != -1:
            return
        else:
            article_html = requests.get(url=url, headers=self.headers).text
            soup = BeautifulSoup(article_html, 'lxml')
            text_article = soup.select('#article-container')  # 主box
            soup1 = BeautifulSoup(str(text_article), 'lxml')
            text_article1 = soup1.select('.column')
            soup2 = BeautifulSoup(str(text_article1), 'lxml')
            global author_data_list
            try:
                soup2.h4.a.string
            except AttributeError:
                return
            else:
                author = soup2.h4.a.string  # 作者姓名
                author_href = soup.h4.a['href']
                # author_data = (author, author_href)
                # # print(author_data)
                # if(souhu_author_data_list.count(author_data) == 0):
                #     souhu_author_data_list.append(author_data)
            # print(author)
            comment = self.souhu_article_comment(href)
            # print(comment)                 #评论
            text_time = soup1.select('.article-info')
            soup4 = BeautifulSoup(str(text_time), 'lxml')
            time = soup4.span.string  # 时间
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
            # print(address[0])                         #地址
            try:
                author_data = (author, author_href, address[0])
            except IndexError:
                author_data = (author, author_href, '无')
            else:
                author_data = (author, author_href, address[0])
                if self.souhu_author_data_list.count(author_data) == 0:
                    self.souhu_author_data_list.append(author_data)
                # print(author_data)
            text_word = soup1.select('.article')  # 文章字数div
            soup5 = BeautifulSoup(str(text_word), 'lxml')
            word = soup5.p.text
            word = word.replace(' ', '')
            word = word.replace('\n', '')
            # print(word)                             #文章
            length = len(word)  # 字数
            # print(length)
            keywords = analyse.extract_tags(word, topK=1, withWeight=False)
            keyword = keywords[0]  # 关键字
            # print(keyword)
            amount = word.count(keyword)  # 关键字出现次数
            # print(amount)
            try:
                total = (title, author, '搜狐', length, type, comment, time, keyword, amount, address[0])
            except IndexError:
                return
            else:
                # cursor = conn.cursor()
                # # 使用 execute()  方法执行 SQL 查询
                # cursor.execute("show databases;")
                # cursor.execute("use `database`;")
                # source = '搜狐'
                # comment_count = 8
                # sql = """insert into `essay`(`id`,`title`,`author`,`source`,`word_count`,`type`,`comment_count`,`publish_time`,`keyword`,`keyword_count`,`publish_address`,`article_link`) values ('%d','%s','%s','%s','%d','%s','%d','%s','%s','%d','%s','%s')"""%(id, title, author, source, length, type, comment_count, time, keyword, amount, address[0],href)
                # try:
                #     # 执行sql语句
                #     cursor.execute(sql)
                #     # 提交到数据库执行
                #     conn.commit()
                #     cursor.close()
                # except:
                #     # Rollback in case there is any error
                #     conn.rollback()
                total = [title, author, '搜狐', length, type, comment, time, keyword, amount, address[0], href]
                self.souhu_article.append(total)
                # print(total)

    # 搜狐网爬取作者信息、订阅数和粉丝数、简介、文章数
    def souhu_author_information(self, name, href, address):
        url = href
        author_html = requests.get(url=url, headers=self.headers).text
        soup = BeautifulSoup(author_html, 'lxml')
        text_author = soup.select('.main')  # 主box
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
            fans = fans[0]  # 订阅数、粉丝数
        # print(fans)
        ex3 = r'''"column_5_text":(.*?),'''
        article_count = re.findall(ex3, author_data[0], re.S | re.M)
        article_count = article_count[0]  # 文章数
        # print(article_count)
        ex4 = r'''"id":"(.*?)"'''
        id = re.findall(ex4, author_data[0], re.S | re.M)
        id = id[0]  # id
        # print(id)
        ex5 = r'''"column_9_text":"(.*?)"'''  # 简介
        introduce = re.findall(ex5, author_data[0], re.S | re.M)
        try:
            introduce1 = introduce[0]
        except IndexError:
            introduce1 = 'None'
        else:
            introduce1 = introduce[0]
        # print(introduce)
        source = "搜狐"
        total = [name, article_count, address, introduce1, fans, source]
        self.souhu_author.append(total)
        # print(total)

    def run(self):
        # #连接数据库
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
        # 使用通用爬虫对url对应的一整张页面进行爬取
        souhu_page_text = requests.get(url=url_sohu, headers=self.headers).text
        souhu_soup = BeautifulSoup(souhu_page_text, 'lxml')
        souhu_text_wrapper = souhu_soup.select('.wrapper-box')  # 主板块的内容
        souhu_text = str(souhu_text_wrapper[0])
        souhu_li_all = []  # 板块的名称
        souhu_li_article = []  # 板块的文章题目
        # 板块列表
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
            # print(s)  # 作者名字和链接
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
