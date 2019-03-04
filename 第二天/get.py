from urllib import request
from fake_useragent import UserAgent
ua = UserAgent().random

url = 'https://www.baidu.com/'

req = request.Request(url)
req.add_header('User-Agent',ua)
response = request.urlopen(req)

print(response.status)
print(response.reason)
print(response.getheaders())
# print(response.read())
html = response.read().decode('utf-8')
# print(html)
# print(response.headers)