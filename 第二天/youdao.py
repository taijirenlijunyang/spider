# 先分析网页有道词典post请求url地址
# http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
from urllib import parse,request
import json
url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
# smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null
formdata = {
    'i': '我的祖国',
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult':'dict',
    'client':'fanyideskweb',
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_CLICKBUTTION',
    'typoResult': 'false',
}
print(type(formdata))
# 先使用urlencode参数转为url编码格式的字符串，然后再使用encode() 方法将字符串转为一个bytes类型
formdata_last = parse.urlencode(formdata).encode('utf-8')
req_header={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
# 创建一个request对象
req = request.Request(url,headers=req_header,data=formdata_last)
response = request.urlopen(req)
print(response.status)
# print(response.read().decode('utf-8'))

json_str = response.read().decode('utf-8')
"""
得到一个json格式的数据类型
json类型的数据是由对象和数组组成的
{
"type":"ZH_CN2EN",
"errorCode":0,
"elapsedTime":1,
"translateResult":[
    [
        {"src":"我的祖国","tgt":"My motherland"}
    ]
                    ]
}
同时这里会有一个坑，那就是json数据类型的数据，键和值都必须是双引号引起来的“”
而不是单引号''
"""

# 将json字符串，转化为python的数据类型（json类型的数据是由对象和数组组成的）
# 对象 -> 字典   数组- >list
data = json.loads(json_str)
print(type(data))
print(data)
translated = data['translateResult'][0][0]['tgt']
print(translated)
