import wordcloud as wc


# tag参数是指进行词云操作的种类，text参数是指该类别中所有关键字组合的字符串（每个关键字需要用空格隔开）
# 需要将数据库中同类新闻的关键字整合起来，形成一个以空格隔开的字符串
def make_wordcloud(text):
    w = wc.WordCloud(
        width=1000,
        height=800,
        background_color='white',
        max_words=100,
        margin=2,
        # colormap='cool',
        font_path="msyh.ttc",
        mode="RGBA",
        collocations=False
    )
    w.generate(text)
    w.to_file(file_path)
