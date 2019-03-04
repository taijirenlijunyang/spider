# requests模块是对urllib的封装，可以实现urllib的所有功能
# 并且api调用更加方便

import requests
from fake_useragent import UserAgent
# url = 'http://www.baidu.com/'
url = 'http://www.sina.com/'
# url:目标url
# params:get请求后面要拼接的参数
"""
param method: 表示发起的请求方式
:param url: 目标url地址
:param params: get请求后面要拼接的参数
:param data: 请求的表单数据，post请求
:param json: 传一个json数据，跟data参数一样
:param headers: 请求头
:param cookies: (optional) Dict or CookieJar object 设置cookie信息，模拟用户请求
:param files: 上传文件
:param auth: 认证信息，一般来讲是账号和密码
:param timeout: 请求超时时间
:param allow_redirects:bool，是否允许重定向
:param proxies: 设置代理，dict
:param verify:  Defaults to ``True``.（是否忽略证书号，默认是buhul，hul为false）
"""


ua = UserAgent().random
req_header = {
    'User-Agent':ua,
}
parmars = {
    'wd':'豆瓣'
}
# response = requests.get(url,params=parmars,headers=req_header)
# 查看能获取什么响应信息
response = requests.get(url,headers=req_header)
# 如果在下面html出现乱码
response.encoding = 'utf-8'  # 根据网页具体编码格式来填写
html = response.text  # 得打解码后的字符串
print(html)
# 如果出现乱码
# response.content.decode('')
b_html = response.content  # 获取bytes类型的数据

code = response.status_code  # 获取状态吗
# print(code)
# response_headers = response.headers  # 获取请求头
#
req_header = response.request.headers  # 请求头
# print(req_header)
# current_url = response.url  # 获取当前请求的url地址

# response.json ：可以将json字符串转为python 类型
