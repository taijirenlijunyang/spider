# 使用requests设置代理
import requests
proxies = {
    'http':'117.91.232.136:9999',  # 使用http代理创建http键，值跟代理
    'https':'116.209.59.237:9999',   # 使用http代理创建http键，值跟代理
}

url = 'http://httpbin.org/get'
response = requests.get(url,proxies=proxies)
print(response.status_code)
print(response.text)