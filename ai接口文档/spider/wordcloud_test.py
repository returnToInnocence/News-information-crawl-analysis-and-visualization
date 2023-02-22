import Word_cloud
import jieba


with open('C:/Users/CCH/Desktop/2.txt', encoding='utf-8') as file:
    t = file.read()

ls = jieba.lcut(t)
text = " ".join(ls)
# print(text)
Word_cloud.make_wordcloud(text, '军事')
