
"""
https://www.baidu.com/s?wd=马云&rsv_spt=1&rsv_iqid=0xc7480d840000cbaa&issp=1&f=3&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg
&rsv_enter=1&rsv_sug3=6&rsv_sug1=4&rsv_sug7=101&rsv_sug2=0&prefixsug=mayun&rsp=2&inputT=4107&rsv_sug4=4824

https://www.baidu.com/s?wd=%E9%A9%AC%E4%BA%91&pn=10
&oq=%E9%A9%AC%E4%BA%91&tn=baiduhome_pg&ie=utf-8&usm=2&rsv_idx=2
&rsv_pq=cb26f99400018ab6&rsv_t=94d2ezB2DHKJiSgNKUtZVdI86IAr0OdlJuFCkdVj5x9Ql46bbj2YxErVI8PHMf3G2Bc5

https://www.baidu.com/s?wd=%E9%A9%AC%E4%BA%91&pn=20
&oq=%E9%A9%AC%E4%BA%91&tn=baiduhome_pg&ie=utf-8&usm=2&rsv_idx=2
&rsv_pq=dbe990850001895b&rsv_t=7537lWQ5t2PgtXC383txj7mseNQwrW9KvExkrtg%2BnjCJrMPBKJnS66DITPvllfw9WPjy
"""

"""
https://www.baidu.com/s?wd=马云 
通过对上面每个页面的观察得到，关键参数
https://www.baidu.com/s?wd=%E9%A9%AC%E4%BA%91&pn=20  # 关键字成为了字节码
在上面的url中，pn=后面所跟的数字就是每个关于关键字所搜索出来的数据在哪个页面上，即第一页为0-9，第二页为10-19
"""
from urllib import parse,request
from fake_useragent import UserAgent


def seacherSpider(k_w,start_page,end_page,user_agent):
    # # quote函数，讲中文转为url能够识别的编码格式
    # quoted = parse.quote(k_w)
    # print(quoted)
    # # unquote函数，讲url使用的编码格式再转为能够读识的汉字
    # unquote = parse.unquote(quoted)
    # print(parse.unquote(quoted))

    for page in range(start_page,end_page+1):  # range左开右闭，所以加1
        # 当批量修改url中的关键参数时，我们可以使用字典来赋值，等号=左边为键，右边为值
        # 讲字典类型的参数，转为url的编码格式
        parmars = {
            'wd':k_w,
            'pn':(page - 1) * 10,
        }
        result = parse.urlencode(parmars)  # Encode a dict or sequence of two-element tuples into a URL query string.
        # print(result)
        # 完成url地址https://www.baidu.com/s?wd=%E9%A9%AC%E4%BA%91&pn=20
        full_url = 'https://www.baidu.com/s?' + result
        # print(full_url)
        # 构造完url之后发起请求
        html = load_page(full_url,user_agent)
        # print(html)
        file_name = '第'+ str(page) + '页' + k_w + '.html'
        save_Page(html,file_name)

def load_page(url,user_agent):
    """对目标url发起请求"""
    # req = request.Request(url)
    # req.add_header('User-Agent',user_agent.random)
    req_header = {
        'User-Agent':user_agent,
    }
    req = request.Request(url,headers=req_header)
    responese = request.urlopen(req,timeout=1)
    if responese.status == 200:
        print('请求成功',responese.url)

        # 请求成功之后返回一个html源码,由于response返回的是二进制的格式，所以对放回结果进行了一个编码
        return responese.read().decode('utf-8')


def save_Page(html,file_name):
    """用来保存获取到的页面源码
    :param html:页面源码
    :param file_name:保存文件的文件名
    """
    with open('baiduseacher/'+file_name,'w') as file:
        file.write(html)
if __name__ == '__main__':
    # 实例化一个ua对象，用来模拟不同浏览器
    user_agent = UserAgent().random
    # 模拟搜索引擎，根据关键字段来获取页面的信息（即：html源码）
    # 输入搜索关键字，即：你想搜索的关键字
    k_w = input('请输入搜索的关键字')
    # 起始页
    start_page = int(input('请输入起始页'))  # python基础，由于input输入为字符串，所以需要转为int类型
    # 截止页
    end_page = int(input('请输入截止页'))
    seacherSpider(k_w,start_page,end_page,user_agent)
