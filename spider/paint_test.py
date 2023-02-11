import matplotlib
import random
import matplotlib.pyplot as plt

# 中文乱码和坐标轴负号处理。
matplotlib.rc('font', family='SimHei', weight='bold')
plt.rcParams['axes.unicode_minus'] = False

# 城市数据。
news_name = ['胡鑫宇遗体发现地金鸡山：山上荆棘密布 紧挨其学校', '上海', '广州', '深圳', '成都']

# # 数组反转。
# news_name.reverse()

# 装载随机数据。
data = [1300, 600, 960, 2300, 3500]
# for i in range(len(news_name)):
#     data.append(random.randint(100, 150))

# 绘图。
fig, ax = plt.subplots(figsize=(17.5, 8))
# fig, ax = plt.subplots()
b = ax.barh(range(len(news_name)), data, height=0.4, color='#6699CC')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("新闻点击量", labelpad=20, fontdict={'fontsize': 18})

# 为横向水平的柱图右侧添加数据标签。
index = 0
for rect in b:
    w = rect.get_width() / 2
    ax.text(w, rect.get_y() + rect.get_height() / 2,
            news_name[index], ha='center', va='center', size='x-large')
    index = index + 1

# 设置Y轴纵坐标上的刻度线标签。
ax.set_yticks(range(len(news_name)))
# ax.set_yticklabels(news_name)
plt.tick_params(labelsize=13)

# 不要X横坐标上的label标签。
plt.yticks(())

plt.title('今日热点新闻', loc='center', fontsize='25',
          fontweight='bold', color='black', fontstyle="italic")

png_path = '今日热点新闻.png'
plt.savefig(png_path)

plt.show()



