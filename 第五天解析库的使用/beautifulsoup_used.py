# beautifulsoup 作用是html/xml中提取数据，会载入整个html 文档，效率会比lxml解析器低
# 举个例子
# 分析网页
"""
1. 是静态还是动态
2. 分页的标签规则
https://hr.tencent.com/position.php?keywords=&lid=0
https://hr.tencent.com/position.php?keywords=&lid=0&start=10
https://hr.tencent.com/position.php?keywords=&lid=0&start=20
https://hr.tencent.com/position_detail.php?id=48206&keywords=&tid=0&lid=0
"""
import requests
from bs4 import BeautifulSoup

def load_page_url(url):
    req_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(url,headers=req_headers)
    if response.status_code == 200:
        print('请求成功')
        # 根据偏移量的构建方式不太好
        # 如果页面源码中，有下一页，那么可以提取该标签的href属性

        next_url = parse_page_data(response.text)
        if next_url != 'javascript:;':
            next_url = 'https://hr.tencent.com/' + next_url
            load_page_url(next_url)
        else:
            print('抓取工作已经完成')
def parse_page_data(html):
    """
    解析页面源码
    :param html:
    :return:
    """
    # features = None:指明bs解析器 默认是lxml
    # lxml: 使用lxml下的html解析器
    # html.parser:是python自带的一个解析器模块
    html_bs = BeautifulSoup(html,features='lxml')
    # 找到职位列表
    # html_bs.find() 查找一个
    """
    findall()的参数,最多前两个
   name=None: 指定你要查找的标签名，可以是一个字符串，正则表达式，或者列表
   attrs={}, 根据属性的值查找标签（dict）{“属性名字”:'值'}
   text=None,可以是一个字符串，正则表达式，查找符合条件的文本内容
    limit=None  限制返回的标签个数
    get_text(): 取标签的文本
    """
    tr_even = html_bs.find_all(name='tr',attrs={'class':'even'})  # 查找所有符合节点的标签，返回列表
    tr_odd = html_bs.find_all(name='tr',attrs={'class':'odd'})  # 查找所有符合节点的标签，返回列表
    for tr in tr_even+tr_odd:  # 连个列表加在一起
        # print(tr)
        job_info ={}
        job_info['title'] = tr.select('td.l.square > a')[0].get_text()  #css选择器 标签名+（选择器的类别），当有两个或者两个以上的类名字时，空格换成.
        # print(job_info['title'])
        # 取出职位的类别
        job_info['type'] = tr.select('td:nth-of-type(2)')[0].get_text()
        # 招聘人数
        job_info['num'] = tr.select('td:nth-of-type(3)')[0].get_text()
        # 地点
        job_info['adress'] = tr.select('td:nth-of-type(4)')[0].get_text()
        # 发布时间
        job_info['publishtime'] = tr.select('td:nth-of-type(5)')[0].get_text()
        # 提取职位详情地址
        detail_url = tr.select('td.l.square > a')[0].attrs['href']
        # print(detail_url)
        # https://hr.tencent.com/position_detail.php?id=48206&keywords=&tid=0&lid=0
        # print(job_info)
        full_url = 'https://hr.tencent.com/' + detail_url
        # 加载详情页的源码,提取相应内容，职位要求和描述
        job_info['content'] = load_data(full_url)
    # 提取下一页的url链接
    # next_page = html_bs.select('a#next')[0].sttrs['href']
    next_url = html_bs.select('a#next')[0].attrs['href']
    print(next_url)
    return next_url
def load_data(html):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(html,headers=req_headers)
    if response.status_code == 200:
        print('加载详情页面')
        # 创建一个对象
        html_bs = BeautifulSoup(response.text,features='lxml')
        # 用css选择器去除li标签
        content_li = html_bs.select('ul.squareli li')
        content = []
        # 将取出的标签放入列表中
        for li in content_li:
            print(li.get_text())
            li_text = li.get_text()
            content.append(li_text)
        return ','.join(content)

if __name__ == '__main__':
    # 目标url
    url = 'https://hr.tencent.com/position.php?keywords=&lid=0&start=0'
    load_page_url(url)
