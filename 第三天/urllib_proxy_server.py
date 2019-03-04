# urllib下使用代理
# http/https
# 一定要使用高度匿名代理
# 隐藏真实ip

# urllib使用代理,就要自己创建方法
from urllib import request
from fake_useragent import UserAgent
# 自定义ProxyHandler的目的是为了设置代理，使用代理取发起请求
# self, proxies=None： proxies对应的是一个字典
proxies = {
    'http':'117.91.232.136:9999',  # 使用http代理创建http键，值跟代理
    'https':'116.209.59.237:9999',   # 使用http代理创建http键，值跟代理
}
# 代理分类
# 1:免费和收费
# 2：代理（西刺，快代理，。。。有免费的也有收费的），收费的（阿布云....）
handler = request.ProxyHandler(proxies)

# 自定义opener

opener = request.build_opener(handler)

#测试地址
url = 'http://httpbin.org/get'
ua = UserAgent().random
req_header = {
    'User-Agent':ua
}

# 创建request对象
# req = request.Request(url,headers=req_header)
response = opener.open(url)
print(response.status)


