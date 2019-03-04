import requests

# 测试接口
url = 'https://httpbin.org/post'

file = {
    'file':open('file.txt','r')
}
print(file)
# 文件上传
response = requests.post(url,files=file)
print(response.text)