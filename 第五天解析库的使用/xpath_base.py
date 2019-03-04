# xpath:可以在xml中查找信息，对xml文档中元素进行遍历和属性的提取
#xml:被设计的目的就是为了传输数据，结构和html非常相似，是一种标记语言
"""
nodename 选取此节点下的所有子节点
/        从根节点开始查找
//        匹配节点，不考虑节点的位置
.        选取当前节点
..        选取当前节点的父节点
@         取标签的属性
a/@href   取标签的数据
@/text()   取标签的文本
a[@class='abc']  根据class属性寻找
a[@id='abc']

a[@id='abc'][last()]  取最后一个id为abc的a标签
a[@id='abc'][postion()<2]  取前两个id为abc的前两个标签
"""
# 例子
# 爬取百思不得姐的声音，用户，标题，时间，点赞量等，音乐下载到本地
# 进去想爬去的页面，分析页面是动态还是静态，通过取页面中找标签来确定。
# http://www.budejie.com/audio/
# http://www.budejie.com/audio/2
# http://www.budejie.com/audio/3
# 分析页面得知，每一页为其对应的页面

import requests
from lxml.html import etree  # 把html转换为xml的文档树
import re,pymysql
def load_page_data(url):
    """
    下载器（根据分页的url获取分页的页面源码）
    :param url:分页url
    :return:
    """
    req_headers={
        'User-Agent':' Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }

    response = requests.get(url,headers=req_headers)
    if response.status_code == 200:
        print('请求成功')
        # with open('bsbdj.html','w') as file:
        #     file.write(response.text)
        result = parse_page_data(response.text)  # 进行了一个判断，看是否有返回值。
        if result:
            # 请求下一页数据
            pattern = re.compile('\d+')
            current_page = re.search(pattern,url).group()
            next_page = int(current_page) + 1
            pattern = re.compile('\d+')
            next_page_url = re.sub(pattern,str(next_page),response.url)
            load_page_data(next_page_url)
# 数据提取
def parse_page_data(html):
    """
    使用xpath从html页面源码中提取数据
    :param html:
    :return:
    """
    # 使用etree.HTML方法，转为xml（element）对象
    html_element = etree.HTML(html)
    autio_list = html_element.xpath('//div[@class="j-r-c"]/div[@class="j-r-list"]/ul/li')  # 使用//表示不论标签在那个位置都可以
    #  autio_list = html_element.xpath('//div[class="j-r-c"]//li') 当确定前面的class下面中，是我们全部的li那么我们也可以省略中间
    print(autio_list)
    print(len(autio_list))
    for items in autio_list:
        # print(items.xpath('.//div[@class="j-r-list-c-desc"]/text()')[0])
        autio_data = {}
        # 去除标题
        autio_data['name'] = items.xpath('.//a[@class="u-user-name"]/text()')[0]
        # 取出内容
        autio_data['content'] = items.xpath('.//div[@class="j-r-list-c-desc"]/text()')[0]
        # 发布时间
        autio_data['publishtime'] = items.xpath('.//span[@class="u-time  f-ib f-fr"]/text()')[0]
        # 点赞数
        autio_data['dianzanshu'] = items.xpath('.//li[@class="j-r-list-tool-l-up"]/span/text()')[0]
        # 差评数
        autio_data['chapingshu'] = items.xpath('.//li[@class="j-r-list-tool-l-down "]/span/text()')[0]
        # 封面
        autio_data['coverImage'] = items.xpath('.//div[@class=" j-audio"]/@data-poster')[0]
        # 音频的url
        autio_data['mp3_url'] = items.xpath('.//div[@class=" j-audio"]/@data-mp3')[0]

        print(autio_data)
        # 下载 音频
        download_audio_by_url(autio_data['mp3_url'],autio_data)
    if len(autio_data) > 0:
        return True
    else:
        return False
def download_audio_by_url(url,autio_data):
    """
    根据音频的url地址下载音频数据
    :param url: 音频的url地址
    :param autio_data :
    :return:
    """
    # 设置请求头
    req_headers = {
        'User-Agent': ' Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    response = requests.get(url,headers = req_headers)
    if response.status_code == 200:
        # print(response.url,"下载成功")
        print(response.url)
        filename = response.url[-17:]
        print(filename)
        print('baisibudejie/'+filename)
        with open('baisibudejie/'+filename,'wb') as file:
            file.write(response.content)
            autio_data['localpath'] = 'baisibudejie/'

        # 存储数据到数据库
        save_data_to_db(autio_data)


def save_data_to_db(autio_data):

    sql = """
               insert into mp3(%s)
               values(%s)
           """ % (','.join(autio_data.keys()), ','.join(["%s"] * len(autio_data))
                  )
    try:
        cursor.execute(sql, list(autio_data.values()))
        mysql_client.commit()
    except Exception as error:
        print(error)
        mysql_client.rollback()


if __name__ == '__main__':
    # 先链接数据库，这样不用在存储数据的时候，每次都去链接
    mysql_client = pymysql.Connect('localhost', 'root', 'abcdqwe', 'baisibudejie', 3306, charset='utf8')
    # 创建游标
    cursor = mysql_client.cursor()
    start_url = 'http://www.budejie.com/audio/1'

    # 调用加载页面吗
    load_page_data(start_url)















