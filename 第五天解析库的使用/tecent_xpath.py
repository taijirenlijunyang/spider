# 首先进入目标url主页，去观察里面是的标签是动态加载的还是静态的
# 分析每一页的url，观察其规律

from lxml.html import etree
import requests




def load_page_url(url):
    req_header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    # 向目标url发起请求
    response = requests.get(url,headers=req_header)
    if response.status_code == 200:
        print('获取成功')
        # 犹豫要提取页面源码中有用的数据和标签，我们重新定义一个url解析函数
        parse_page_data(response.text)




def parse_page_data(html):
    """
    解析提取页面源码中有用的信息
    :param html: 页面源码
    :return:
    """
    xml_html = etree.HTML(html)
    html_even = xml_html.xpath('//td')
    print(html_even)
    for items in html_even:
        print(type(items))
        # print(items)
        # 获取标题
        job_info = {}
        job_info['type'] = items.xpath('')
        print(job_info['type'])




if __name__ == '__main__':
    # 目标url
    url = 'https://hr.tencent.com/position.php?keywords=&lid=0&start=0'
    load_page_url(url)