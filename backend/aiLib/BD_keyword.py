import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models


def analyze(text):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305

        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.KeywordsExtractionRequest()
        params = {
            'Text': text,
            'Num': 5
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个KeywordsExtractionResponse的实例，与请求对象对应
        resp = client.KeywordsExtraction(req)
        # 输出json格式的字符串回包
        # print(resp.to_json_string())
        j = json.loads(resp.to_json_string())
        # return j['Keywords']
        lk = j['Keywords']
        keys = []
        for i in lk:
            keys.append(i['Word'])
        # 关键字统计返回的是一个列表
        return keys

    except TencentCloudSDKException as err:
        print(err)

#     content = file.read()

# content = "2月23日，据时间视频报道，2月21日，浙江台州一女生考研结束查分，看到成绩后激动到晕倒住院。  " \
#               "妈妈蒋女士说，女儿在外租房复习，一整年没有回家。“自己租了一个房子，一个人在努力。也没有手机，我们打电话，她都不接”。 " \
#               "蒋女士说，考完研究生后就回老家了，查分的时候小孩子一激动就晕倒了，她赶紧将女儿送去医院，目前女儿已经清醒，没有大碍。“都没事了，医生查了什么事都没有。”  " \
#               "对此，网友表示，“孩子还是压力太大了”，“祝福女生，祝她有光明的未来”，“成绩这么高，真厉害啊”。 【来源：九派新闻综合时间视频、网友评论】 "
#
#
# k = analyze(content)
#
# print(k)

# print(content)
