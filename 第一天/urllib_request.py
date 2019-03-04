######## 如果要添加请求头，就需要创建一个request对象
from urllib import request
# 创建一个request对象时的参数设置
# url:目标url
# data=None: 如果为None 为一个get请求，反之为post请求
# headers={},对应字典类型，这是请求头参数
# method=None：设置请求方式（GET或者POST）

# 设置请求头信息
# 最常见的请求头参数:User-Agent,refere,cookie.(当遇到得不到数据时，要依次添加这三个参数，依次来查看结果。)
req_headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

# 目标url
req_url = 'http://www.eduxiao.com/zuowen1/'

# 根据请求头去创建一个request对象
req = request.Request(url=req_url,headers = req_headers,method='GET')
print(req)

# 另一个种方式 添加请求头参数 add_heerder()
req.add_header('Referer','https://pos.baidu.com/wh/o.htm?ltr=')

# 获取request对象请求头中的设置的参数
refere = req.get_header('Referer')
print('Referer',refere)

# 根据构建的request对象，发起请求。
response = request.urlopen(req)
html = response.read()
# print(html)
html_str = html.decode('gb2312')
# print(html_str)
print(type(html_str))
print(response.getheaders())  # 获取响应头
print(response.status)  # 获取状态码
print(response.url)  # 获取响应url地址

# 将获取的html写入本地
with open('req_html.html','w') as file:
    file.write(html_str)
