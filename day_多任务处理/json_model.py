import json

# 讲json字符串转化为python数据类型
json.loads()

# 讲python数据类型转化为字符串
# ensure_ascii=True 转换的时候默认使用ascii码
# 讲 ensure_ascii=False，表示不使用ascii编码，使用unicode编码
json.dumps()

# 将本地的json文件加载出来，转换为python数据类型
json.load()

#将 python类型转换为json字符串，并且存储到本地
# 讲 ensure_ascii=False，表示不使用ascii编码，使用unicode编码
json.dump()