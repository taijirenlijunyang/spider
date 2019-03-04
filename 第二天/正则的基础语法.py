# 由于在爬取html之后，要提取有用的url子链接，我们要从一堆源码中找出有用的url就需要用正则取查找


import re

# 将正则表达式，构建成一个pattern对象
sub_str = 'abcdefabcd'
pattern = re.compile('b')

# 从字符串起始位置开始匹配，开头就必须符合正则规则，
# 从起始位置开始匹配，如果匹配到了就返回结果，否则返回None
result = re.match(pattern,sub_str)
print(type(result))
if result:
    print(result.group())
# print(result)

# search 在整个字符串中进行匹配，同样是单次匹配，如果有就返回，否则返回None
re_search = re.search(pattern,sub_str)
print(re_search)
print(re_search.group())

# 在整个字符串中进行匹配，匹配出所有符合正则规则的结果，以裂变形式返回。
re_findall = re.findall(pattern,sub_str)
print('re_findall',re_findall)

# 在整个字符串中进行匹配，匹配出所有符合正则规则的结果，返回的是一个迭代器
re_finditer = re.finditer(pattern,sub_str)
print('re_finditer',re_finditer)
for i in re_finditer:
    print(i.group())

# sub 替换
"""
sub()函数参数
:param:pattern: 正则规则
:param:repl，要替换的字符串
:param：string，原始字符串
"""
# 加入知道所搜索的结果页面，每页显示10条
url = 'https://www.baidu.com/s?kw=aaa&pn=30'
# 那当进行下一页的操作是，我们只需要把pn后的页数更改了就行了
pattern = re.compile('pn=\d+')
re_sub = re.sub(pattern,'pn=50',url)
print(re_sub)

# 字符串的分割re.split()
# pattern = re.compile('=')  # 单个等号分割
pattern = re.compile('[:=&]')  # []里面的每个都能进行匹配
re_split = re.split(pattern,url)
print('re_split',re_split)

sub_html = """
<div class="threadlist_title pull_left j_th_tit ">
    
    
    <a rel="noreferrer" href="/p/6044133651" title="转贴:健康是人一生最大的财富,送给大家店养生小知识【水生美植物..." target="_blank" class="j_th_tit ">转贴:健康是人一生最大的财富,送给大家店养生小知识【水生美植物...</a>
</div>
"""

# re.S让点可以匹配包括换行符的任意字符
pattern = re.compile('<div.*?class="threadlist_title pull_left j_th_tit ">'+
                     '.*?<a.*?href="(.*?)".*?</div>',re.S)  # ()使用组
result = re.findall(pattern,sub_html)  # 爬虫里面用的最多的正则方法
print(result)