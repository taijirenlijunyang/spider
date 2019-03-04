from fake_useragent import UserAgent
from urllib import  request
ua = UserAgent()
print(ua.random)
url = 'http://www.eduxiao.com/zuowen1/'

req = request.Request(url)
req.add_header('User-Agent',ua.random)
response = request.urlopen(req)
html  = response.read().decode('gb2312')
print(html)
print(response.status)