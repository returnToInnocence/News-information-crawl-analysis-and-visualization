import requests
import json

API_KEY = "gyv0NMrt30MsfMFq2NLGrGkm"
SECRET_KEY = "NnA6iYc1idjjiFSzm52YHO753pEEIsGs"


def txt_main(text):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary?charset=UTF-8&access_token=" + get_access_token()

    payload = json.dumps({
        "content": text,
        "max_summary_len": 150,
        "title": "美军售激增 有分析称美军火商未来3年将多赚730亿美元"
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
    with open('C:/Users/CCH/Desktop/2.txt', encoding='utf-8') as file:
        content = file.read()
    text_main = txt_main(content)
    print(text_main)


