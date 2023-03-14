import matplotlib
import matplotlib.pyplot as plt


# news_name是指新闻标题组成的列表，click_name是指这些新闻的点击量形成的列表
def paint(news_name, click_num):
    # 中文乱码和坐标轴负号处理。
    matplotlib.rc('font', family='SimHei', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False

    # 绘图。
    fig, ax = plt.subplots()
    pic = ax.barh(range(len(news_name)), click_num, color='#6699CC')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlabel("新闻点击量", labelpad=20, fontdict={'fontsize': 18})

    # 为横向水平的柱图中添加数据标签。
    index = 0
    for rect in pic:
        w = rect.get_width() / 2
        ax.text(w, rect.get_y() + rect.get_height() / 2, news_name[index], ha='left', va='center')
        index = index + 1

    # 设置Y轴纵坐标上的刻度线标签。
    ax.set_yticks(range(len(news_name)))

    # 设置刻度字体大小
    plt.tick_params(labelsize=13)

    # 不要y轴上的label标签。
    plt.yticks(())

    plt.title('今日热点新闻', loc='center', fontsize='25',
              fontweight='bold', color='black', fontstyle="italic")

    png_path = r'C:\Users\dell\Desktop\数据库课程设计GitHub同步\backend\static\今日热点新闻.png'
    plt.savefig(png_path)
    return png_path

