import Word_cloud
import jieba


# with open('C:/Users/CCH/Desktop/2.txt', encoding='utf-8') as file:
#     t = file.read()

keyWord = "你好 好哒 谢谢 没事 嗯嗯 对的 没问题 谢谢 谢谢 谢谢 谢谢 谢谢 谢谢 谢谢 哦哦 啊"

# ls = jieba.lcut(t)
# text = " ".join(ls)
# print(type(text))
Word_cloud.make_wordcloud(keyWord, "搜狐新闻")
