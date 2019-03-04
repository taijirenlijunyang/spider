import requests

"""
url, 目标url
data=None,  post 请求上传的表单数据 
"""
# 拉勾网
url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'

form_data = {
    'first':	'true',
    'pn':1,
    'kd':	'python'
}
req_header = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
}
response = requests.post(url,data=form_data,headers= req_header)
print(response.status_code)
print(response.text)
dat = response.text
print(type(dat))
# 可以将返回的json字符串转为python数据类型
data = response.json()
print(type(data))
