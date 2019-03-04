from urllib import request
import ssl
url = 'http://www.baidu.com'
# url: 请求地址
# data: 请求的方式，默认为None即为get请求
# timeout： 响应时间
# context=None; 设置就表示忽略未认证的ssl证书
# 需要忽略时：
context = ssl._create_unverified_context()
# req = request.urlopen(url,timeout=1,context=context)  # 里面参数有一个context
# 使用urlopen()有个缺点：即不能够携带请求头，所有需要创建一个Request对象来满足
# print(response.read())
# 携带请求头，创一个request对象
header = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
}

req = request.Request(url,headers=header)
print(req)
req.add_header('Refere','https://www.baidu.com/')
# print('*')

response = request.urlopen(req)

# print(response.getheaders())
# Reqeust() 参数最常用的为前三个
# url,
# data=None,
# headers={},
# origin_req_host=None,
#  unverifiable=False,
# method=None
# 添加参数有两个方法
# 1: 创建字典，用来写出请求头中参数
# 2: 调用Request.add_header(),通过键+逗号+值来添加
html = response.read().decode('utf-8')
print(html)
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))
print(response.url)
print(response.reason)