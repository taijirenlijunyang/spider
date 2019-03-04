from urllib import  request
# 导入这个模块是为了创建一个context，忽略未认证证书
import ssl
# 1 指定目标URL
# data = None:默认为None表示是一个get请求
#             如果不为None,表示一个post请求
# timeout：指定超时时间
# cafile = None:可以指定证书文件（一般情况下用不到这个参数）
# capath = None: 指明证书路径
# cadefault = False: 是否使用默证书

# context = None: 赋值则表示忽略未认证的sll证书 如果出现证书错误，就需要设置了

url = 'http://www.eduxiao.com/zuowen1/'
#根据url发起请求的到响应结果

# 创建context目的是为了忽略未认证的ca
context = ssl._create_unverified_context() # 创建一个为认证的ssl

response = request.urlopen(url=url,timeout=1,context=context)


# 从响应结果中我们能得到什么数据
# 获取页面的二进制文件
html = response.read()
# print(html)
# 讲二进制数据转换为字符串
html_str = html.decode('gb2312')
# print(html_str)
# 讲获取的html页面源码，写入本地文件
with open('page.html','w') as file:
    file.write(html_str)

# 获取响应状态码
status = response.status
print(status)

# 获取所有响应头信息
response_headers = response.getheaders()
print(response_headers)
# 获取指定响应头信息
# 获取响应的文本长度
Content_Length = response.getheader('Content-Length')
print(Content_Length)

# 获取响应的原因
response_reason = response.reason
print(response_reason)

# 获取响应的请求地址
response_url = response.url
print(response_url)

# 反爬的时候
# 如果不指定user-agent:python3.5-urlib/3.py(比如),如果不指定就是这个字符串