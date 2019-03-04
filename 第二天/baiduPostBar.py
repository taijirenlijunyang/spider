# 目标获取百度贴吧中帖子的所有图片
# step1:分析贴吧z中分页的url地址规律，要根据url构造请求
"""
https://tieba.baidu.com/f?ie=utf-8&kw=%E7%BE%8E%E5%A5%B3&fr=search 第一页
https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=50  第二页
https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=100  第三页
1.通过分析url得到，每页有50各项
2.发现第一页和后面其他页面的url上不同有在于关键字kw后，fr=search
3.尝试把第一页url改为https://tieba.baidu.com/f?ie=utf-8&kw=%E7%BE%8E%E5%A5%B3&pn=0，然后通过浏览器来认证是否正确
"""
# step2:获取分页中帖子详情的url地址，要根据url构造请求


# step3：从详情页面中获取图片的地址，根据url构造请求
from urllib import request, parse
from fake_useragent import UserAgent
import re


def PostBarSpider(name, start_page, end_page):
    # https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=100 分析url来写url中关键参数
    for page in range(start_page, end_page + 1):
        parmars = {
            'kw': name,
            'ie': 'utf-8',
            'pn': (page - 1) * 50,
        }
        # 将字典类型参数，转化为url编码格式的字符串
        result = parse.urlencode(parmars)
        # 拼接完成url地址
        full_url = 'https://tieba.baidu.com/f?' + result
        # print(full_url)
        # 根据分页的url地址，发起请求，得到响应结果，提取html页面源码
        html = load_url(full_url, user_agent)
        # 从页面源码中匹配出帖子详情的url地址
        post_bar_detail_info = post_bar_detail(html)
        for item in post_bar_detail_info:
            # https://tieba.baidu.com/p/6042086459 随便点击一个标题得到一个url地址
            # 每个子标题的URL
            detail_url = 'https://tieba.baidu.com' + item[0]
            # 每个帖子的标题
            title = item[1]
            print('正在获取' + title + '帖子详情')
            print(title + '帖子url地址' + detail_url)
            # 根据帖子详情的url地址发起请求，获取到页面源码
            html = load_url(detail_url,user_agent)

            pic_url = teizi_detail_imageurl(html)
            download_image(pic_url)
def load_url(url, user_agent):
    """
    :param req_heaer:请求头
    :param url: 目标url
    :return: 返回html源码
    """
    # 设置请求头
    req_header = {
        'User-Agent': user_agent
    }
    # 构造一个request对象
    req = request.Request(url, headers=req_header)
    # 发起请求
    response = request.urlopen(req)
    if response.status == 200:
        print('发起请求成功')
        return response.read().decode('utf-8')


def post_bar_detail(html):
    """
    使用正则从每个分页的页面源码中，提取帖子的详情的url地址
    ：:param:html : 每一个分页页面源码
    :return:
    """
    # 通过观察页面源码得到，每个标题为a标签下的href中，但是a标签很多，所以向上一级得到它的上级元素。
    # sub_html = """
    # <div class="threadlist_title pull_left j_th_tit ">
    #
    #
    #     <a rel="noreferrer" href="/p/6044133651" title="转贴:健康是人一生最大的财富,送给大家店养生小知识【水生美植物..." target="_blank" class="j_th_tit ">转贴:健康是人一生最大的财富,送给大家店养生小知识【水生美植物...</a>
    # </div>
    # """
    # 正则表达式 pattern
    # pattern = re.compile('<div.*?class="threadlist_title pull_left j_th_tit ">'
    #                      + '.*?<a.*?href="(.*?)".*?</div>',re.S)
    # 正则表达式，同时匹配出标题
    pattern = re.compile('<div.*?class="threadlist_title pull_left j_th_tit ">'
                         + '.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?</div>', re.S)
    result = re.findall(pattern, html)
    # print(result)
    return result

def teizi_detail_imageurl(html):
    """
    根据正则从帖子详情页的html源码中，提取图片的地址
    :param html: 每个帖子的url地址
    :return:
    """
    #<img class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=56338251584e9258a63486e6ac82d1d1/8f2bd40735fae6cd2499c15401b30f2442a70fd1.jpg" size="55786" changedsize="true" width="560" height="943">
    pattern = re.compile('<img.*?class="BDE_Image".*?src="(.*?)".*?>',re.S)
    result = re.findall(pattern,html)
    print('pic链接',result)
    return result

def download_image(pic_url):
    """
    根据图片的url地址发起请求，获取图片的二进制数据，进行本地存储
    :param pic_url: 图片的url
    :return:
    """
    for image_url in pic_url:
        req = request.Request(image_url)
        req.add_header('User-Agent',user_agent)
        response = request.urlopen(req)
        if response.status == 200:
            filename = response.url[-20:]
            with open('postbarpic/'+filename,'wb') as file:
                file.write(response.read())
                print(filename,'下载完成')


if __name__ == '__main__':
    # 实例化一个ua对象，用来模拟不同的浏览器
    user_agent = UserAgent().random
    # 输入贴吧名称
    name = input('输入贴吧的名称')
    # 起始页
    start_page = int(input('输入起始页'))
    # 截止页
    end_page = int(input('输入截止页'))
    PostBarSpider(name, start_page, end_page)
