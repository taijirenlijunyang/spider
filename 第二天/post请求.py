# 测试接口，https://httpbin.org/post
from urllib import request, parse
from fake_useragent import UserAgent

url = 'https://httpbin.org/post'
# 表单数据
postdata = {
    'name': 'xxx',
    'age': 18,
    'gender': '女',
}

# 先使用urlencode参数转为url编码格式的字符串，然后再使用encode() 方法将字符串转为一个bytes类型
result = parse.urlencode(postdata).encode('utf-8')
#
# response = request.urlopen(url,data=result)
# print(response.status)
# print(response.read().decode('utf-8'))

# 设置请求头
user_agent = UserAgent().random
req_header = {
    'User-Agent': user_agent,
}
req = request.Request(url, headers=req_header, data=result)
response = request.urlopen(req)
print(response.status)
print(response.read().decode('utf-8'))
