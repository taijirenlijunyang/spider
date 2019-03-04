# urllib中parse模块主要是实现url的解析，合并，编码和解码

from urllib import parse


# 实现了url的识别和分段
# 随便写一个url
url = 'https://www.study.com/daxuesheng?name=lisi#123'

# url: 要解析和拆分的url
# scheme='':设置协议（在url没有协议的情况下才会生效）
# llow_fragments=True： 是否要忽略锚点，默认为True，表示不忽略
# 拆分
result = parse.urlparse(url)
print(result)
# 测试结果
"""
通过测试结果，我们可以选择相应的内容
ParseResult(
    scheme='https' :协议
    netloc='www.study.com'  ： 域
    path='/daxuesheng' ：路径
    params=''  ： 可选参数
    query='name=lisi' ：查询参数
    fragment='123'  ：锚点
)
"""
# 通过调用，选取其中某一个值
print(result.scheme)


# 实现url的组合
data = [content_str for content_str in result]  # 列表推导
print('拼接')
full_url = parse.urlunparse(data)  # 其中要注意的是，data是个可迭代对象，其中含有url的六个组成部分。
print(full_url)


# parse.urljoin 需要传入一个基类url,根据基类url讲某一个不完整的url拼接完整
unfull_url = '/p/38494'
base_url = 'https://www.study.com/daxuesheng?name=lisi#123'
full_url = parse.urljoin(base_url,unfull_url)
print('urljoin',full_url)

# 序列化
# parse.urlencode()复习，将字典类型的参数，序列化为url的编码格式的字符串
parmars = {
    'name':'王老板',
    'age':24
}
result = parse.urlencode(parmars)
print('parse.urlencode：',result)

# parse.parse_qs()将url编码格式的字符串，转为字典类型
result = parse.parse_qs(result)
print('parse.parse_qs:',result)
# parse.parse_qs: {'age': ['24'], 'name': ['王老板']} 看出虽然反序列化了，但是键所对应的值为列表

# 可以将中文字符转为url编码格式
k_w = '小李'
result = parse.quote(k_w)
print('parse.quote:',result)
#parse.quote: %E5%B0%8F%E6%9D%8E


# 讲url编码格式的字符串，进行解码
result = parse.unquote(result)
print('parse.unquote:',result)



# urlencode 和 urljoin是经常使用的。