# web客户端验证
import requests

# 设置认证信息

auth = ('username','password')

url = '192.168.1.1'  # 假设是这个页面需要用户认证信息

response = requests.post(url,auth=auth)
print(response.status_code)