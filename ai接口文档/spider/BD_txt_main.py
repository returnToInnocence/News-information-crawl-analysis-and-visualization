import requests
import json

API_KEY = "gyv0NMrt30MsfMFq2NLGrGkm"
SECRET_KEY = "NnA6iYc1idjjiFSzm52YHO753pEEIsGs"


def txt_main(text):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary?charset=UTF-8&access_token=" + get_access_token()

    payload = json.dumps({
        "content": text,
        "max_summary_len": 150,
        "title": "女生考研429分激动晕倒，妈妈：住院了，一整年没有回家，没用手机，很辛苦"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    j = json.loads(response.text)
    # 文章摘要返回的是字符串
    return j['summary']

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    # with open('C:/Users/CCH/Desktop/2.txt', encoding='utf-8') as file:
    #     content = file.read()
    content = "2月23日，据时间视频报道，2月21日，浙江台州一女生考研结束查分，看到成绩后激动到晕倒住院。  " \
              "妈妈蒋女士说，女儿在外租房复习，一整年没有回家。“自己租了一个房子，一个人在努力。也没有手机，我们打电话，她都不接”。 " \
              "蒋女士说，考完研究生后就回老家了，查分的时候小孩子一激动就晕倒了，她赶紧将女儿送去医院，目前女儿已经清醒，没有大碍。“都没事了，医生查了什么事都没有。”  " \
              "对此，网友表示，“孩子还是压力太大了”，“祝福女生，祝她有光明的未来”，“成绩这么高，真厉害啊”。 【来源：九派新闻综合时间视频、网友评论】 "
    text_main = txt_main(content)
    print(text_main)


