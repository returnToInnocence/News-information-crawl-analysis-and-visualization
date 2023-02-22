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

# 普通用户登录接口测试
def loginUserTest():
    httpApi = HttpApiTest()
    # 成功情况
    res = httpApi.testPost("http://localhost:5000/login/", data={
        "user_id": 18031589519,
        "user_password": "123",
        "user_permission": 0
    })
    print(res)
    # 用户不存在情况
    res = httpApi.testPost("http://localhost:5000/login/", data={
        "user_id": 0,
        "user_password": "123",
        "user_permission": 0
    })
    print(res)
    # 密码错误情况
    res = httpApi.testPost("http://localhost:5000/login/", data={
        "user_id": 0,
        "user_password": "0",
        "user_permission": 0
    })
    print(res)

# 管理员登录接口测试
def loginAdmainTest():
    httpApi = HttpApiTest()
    # 成功情况
    res = httpApi.testPost("http://localhost:5000/login/", data={
        "user_id": 1,
        "user_password": "1",
        "user_permission": 1
    })
    print(res)
    # 密码错误情况
    res = httpApi.testPost("http://localhost:5000/login/", data={
        "user_id": 1,
        "user_password": "0",
        "user_permission": 1
    })
    print(res)


def registerTest():
    httpApi = HttpApiTest()
    res = httpApi.testPost("http://localhost:5000/register/", data={
        "user_id": 15903154288,
        "user_name": "李虹均2",
        "user_password": "123",
    })
    print(res)

if __name__ == '__main__':
    pass
    # 通过
    # loginUserTest()
    # loginAdmainTest()
    # registerTest()
    # 实例化对象
    # httpApi = HttpApiTest()
    # res = httpApi.testGet("http://localhost:5000/", data={
    #     "id": 1
    # })
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
    # print(res)
