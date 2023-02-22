# 接口测试
import requests


# 发http请求，做接口单元测试
class HttpApiTest:

    # 测试delete请求方式（删除接口)
    def testDelete(self, url, data={}):
        res = requests.delete(url, params=data)
        return res.text

    # 测试put请求方式（修改接口)
    def testPut(self, url, data={}):
        res = requests.put(url, data=data)
        return res.text

    # 测试post请求方式（插入接口)
    def testPost(self, url, data={}):
        res = requests.post(url, data=data)
        return res.text

    def testGet(self, url, data={}):
        res = requests.get(url, params=data)
        return res.text


if __name__ == '__main__':
    # 实例化对象
    httpApi = HttpApiTest()
    res = httpApi.testGet("http://localhost:5000/", data={
        "id": 1
    })
    # res = httpApi.testPost("http://localhost:5000/insert/", data={
    #     "id": 4,
    #     "email": "第四个测试邮箱",
    #     "password": "第四个测试密码"
    # })
    # res = httpApi.testPut("http://localhost:5000/update/", data={
    #     "id": 1,
    #     "password": "第一个的密码被我改了"
    # })
    # res = httpApi.testDelete("http://localhost:5000/delete/", data={
    #     "id": 4
    # })
    print(res)
