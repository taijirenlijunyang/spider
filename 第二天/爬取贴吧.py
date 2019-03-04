from urllib import request,parse
import re
from fake_useragent import UserAgent

def PostBarSpider(k_w,start_page,end_page):
    """
    # 主程序
    :param k_w: 关键字
    :param start_page: 爬取开始的页面
    :param end_page: 爬取截止页面
    :return:
    """

    for page in range(start_page,end_page+1):
        """
        http://tieba.baidu.com/f?ie=utf-8&kw=%E7%8B%97%E7%8B%97&fr=search&red_tag=o2385813203
        http://tieba.baidu.com/f?kw=%E7%8B%97%E7%8B%97&ie=utf-8&pn=50
        http://tieba.baidu.com/f?kw=%E7%8B%97%E7%8B%97&ie=utf-8&pn=100
        通过观察不同页面的url后得到，关键字一样，只是在pn上，递加了50，即第一页为0,输入pn=0后也能得到第一页
        """

        parmas = {
            'kw':k_w,
            'pn':(page-1)*50
        }
        result =  parse.urlencode(parmas)
        full_url = 'http://tieba.baidu.com/f?' + result
        # print(url)
        html = load_url(full_url)

        zi_url = zi_title(html)
        # 由于得到的zi_url是一个列表套元组，元组里面第一个为编号，第二个为标题
        for item in zi_url:
            zi_detail = 'http://tieba.baidu.com' + item[0]  # 得到每个页面上每个标题的url
            result = load_url(zi_detail)  # 在此发起请求得到每个子标题页面的源码
            # print('子标题的页面源码')
            # 得到每个子标题中的图片url
            image_url = get_zi_detail_image(result)
            # print('image_url',image_url)
            # 传入一个url列表
            download_image(image_url)

# 组成好的url发起请求
def load_url(url):
    # 创建请求头
    req_header = {
        'User-Agent':user_agent,
    }
    # 创建request对象
    req = request.Request(url,headers=req_header)
    response = request.urlopen(req)
    if response.status == 200:
        # print('请求成功')
        # print(response.url)
        return response.read().decode('utf-8')

# 在获取的每页中标题的url
def zi_title(html):
    """
    # 通过页面源码，获取每页中子标题的url
    :param html: 每页源码html
    :return:
    """
    """
    <div class="threadlist_title pull_left j_th_tit ">
    
    
    <a rel="noreferrer" href="/p/6043021303" title="来啦，你在吗" target="_blank" class="j_th_tit " clicked="true">来啦，你在吗</a>
</div>
    """
    # 编写正则表达式
    pattern = re.compile('<div.*?class="threadlist_title pull_left j_th_tit ">'+
                         '.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?</div>',re.S)
    result = re.findall(pattern,html)
    return result

# 由每个子标题的页面源码找到图片的url
def get_zi_detail_image(html):
    """
    <img class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=ad8bd6f1144c510faec4e21250582528/ff1190ef76c6a7efe4d4a01ff3faaf51f3de661c.jpg"
    size="95906" changedsize="true" width="560" height="731">
    :param url:
    :return:
    """
    pattern = re.compile('<img.*?class="BDE_Image".*?src="(.*?)".*?>',re.S)
    result = re.findall(pattern,html)
    return result

# 下载图片并保存
def download_image(url):
    # 创建请求头
    req_header = {
        'User-Agent': user_agent,
    }
    print('正在下载图片到本地')
    # 创建request对象
    for image_url_item in url:
        req = request.Request(image_url_item, headers=req_header)
        response = request.urlopen(req)
        # print(response)
        # print('response.url',response.url)
        filename = response.url[-20:]
        if response.status == 200:
            with open('postbarpic/'+filename,'wb') as file:
                file.write(response.read())

if __name__ == '__main__':
    user_agent = UserAgent().random
    k_w = input('请输入要爬取的吧：')
    start_page = int(input('开始爬取的页面：'))
    end_page = int(input('截止页：'))
    PostBarSpider(k_w,start_page,end_page)