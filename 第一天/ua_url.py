from urllib import request

import random

url = "http://www.httpbin.org/get"

# 写一个浏览器标识，用来模拟使用不同浏览器来访问
ua_list = [
    "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS... "
]

# 使用随机函数，从列表中随机获取一个浏览器的ua
user_agent = random.choice(ua_list)
print(user_agent)
# 构造Request请求对象
req = request.Request(url)

# 可以通过调用Request.add_header() 添加/修改一个特定的header
req.add_header('User-Agent',user_agent)  # 这样ua不同就可以成为使用不同的浏览器发起请求了
print(req.headers)
# get_header()的字符串参数，第一个字母大写，后面的全部小写。
print(req.get_header('User-agent'))
# # 也可以写字典的方式添加UA
# header = {
#     'User-Agent':user_agent,
# }
# print(header)
# req = request.Request(url,headers=header)
# print(req.headers)

# 发起请求，获取服务器响应
respoense = request.urlopen(req)

# 读取响应结果
html = respoense.read().decode('utf-8')
print(html)