from fake_useragent import UserAgent
from urllib import request
ua = UserAgent().random
# print(ua)
url = 'https://www.baidu.com/'
req = request.Request(url)
req.add_header('User-Agent',ua)
response = request.urlopen(req,timeout=1)
print(response.status)
print(req.get_header('Referer'))   # 因为没有添加 所以为None
print(response.url)