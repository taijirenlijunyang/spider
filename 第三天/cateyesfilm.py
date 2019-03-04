from urllib import request, parse
import re,pymysql
from fake_useragent import UserAgent
"""
首页 https://maoyan.com/board/4
第二页 https://maoyan.com/board/4?offset=10
第三页 https://maoyan.com/board/4?offset=20
"""


def catEyeFilmSpider(url):
    # 发起请求，获取页面源码
    html = get_html(url)
    # print(html)
    # 解析页面的源码，拿到需要的信息
    movies_info = get_zi(html)
    if len(movies_info) > 0:
        for movies_detail in movies_info:
            # print(movies_detail)
            moviedata = {}
            # 排名
            moviedata['rank'] = int(movies_detail[0])
            # 影片封面
            moviedata['coverImage'] = movies_detail[1]
            # 电影名称
            moviedata['name'] = movies_detail[2]
            #  主演
            moviedata['actor'] = movies_detail[3].replace('\n','').replace('主演：','').replace(' ','')
            # 上映时间
            moviedata['publishtime'] = movies_detail[4].replace('上映时间','')
            # 分数
            moviedata['score'] = float(movies_detail[5] + movies_detail[6])

            save_data(moviedata)
        # 如何去构造下一页的链接和什么时候应该停止
        # 获取当前页面的偏移量即页数
        #  第一种方法是找出当前页面的页码，然后提取出来在做相加，然后和指定的url进行结合
        pattern = re.compile('.*?offset=(\d+)',re.S)
        current_page = int(re.findall(pattern,url)[0])
        next_page = current_page + 10
        next_url = 'https://maoyan.com/board/4?offset=' + str(next_page)
        # 第二种方法是直接替换
        # pattern = re.compile('offset=\d+')
        # re.sub(pattern,'offset='+str(next_page),url)
        # 循环调用函数自身
        catEyeFilmSpider(next_url)

    else:
        print('已经爬取完成')
def get_html(url):
    """
    获取目标url，html源码
    :param url: 目标url
    :return:
    """
    req_header = {
        "User-Agent": user_agent.random
    }

    req = request.Request(url, headers=req_header)
    response = request.urlopen(req)
    if response.status == 200:
        print('请求成功')
        return response.read().decode('utf-8')


def get_zi(html):
    """
    得到我们想要得到的有用信息，特别注意的就是静态页面要取的部分，一定要看页面网页查看的源码是否和加载之后的一样。
    :param html: 每一页的页面源码,
    :return:
    """
    pattern = re.compile('<dd>.*?<i.*?>(.*?)</i>' +
                         '.*?<img.*?data-src="(.*?)".*?>' +
                         '.*?<p.*?>.*?<a.*?>(.*?)</a>' +
                         '.*?<p.*?>(.*?)</p>' +
                         '.*?<p.*?>(.*?)</p>' +
                         '.*?<i.*?>(.*?)</i>' +
                         '.*?<i.*?>(.*?)</i>' +
                         '.*?</dd>',re.S)
    # print('z正则表达式')
    result = re.findall(pattern, html)
    print(result)
    return result


def save_data(moviedata):
    """
    存储数据
    :param moviedata:
    :return:
    """
    sql = """
           insert into maoyantop100(%s)
           values(%s)
       """ % (','.join(moviedata.keys()), ','.join(["%s"] * len(moviedata))
              )
    try:
        cursor.execute(sql, list(moviedata.values()))
        mysql_client.commit()
    except Exception as error:
        print(error)
        mysql_client.rollback()
if __name__ == "__main__":
    # 连接数据库
    mysql_client = pymysql.Connect('localhost', 'root', 'abcdqwe', 'maoyan', 3306, charset='utf8')
    # 创建游标
    cursor = mysql_client.cursor()

    # top100,url地址
    url = 'https://maoyan.com/board/4?offset=0'
    user_agent = UserAgent()
    catEyeFilmSpider(url)
