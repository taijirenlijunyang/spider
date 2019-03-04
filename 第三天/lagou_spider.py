# url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
from urllib import request, parse,error
import json, pymysql, time
from fake_useragent import UserAgent


# formdata = {
#  'first': 'true',
#  'pn': '1', 页码
#  'kd': 'c++'  关键字
# }

def LaGouSpider(url, formdata):
    """

    :param url:
    :param formdata:
    :return:
    """
    # 接受响应的结果,会得到一个json格式的数据
    response_data = load_data_page(url, formdata)
    # 转为数据为python类型的数据
    data = json.loads(response_data)
    print(data)
    print(type(data))
    # print(data)
    # 拿到职业信息
    if data['success']:
        print('请求成功')
        positionJson = data['content']['positionResult']['result']
        for jobinfo in positionJson:
            job_data = {}
            # 职位标题
            job_data['positionName'] = jobinfo['positionName']
            # 发布时间
            job_data['publishTime'] = jobinfo['createTime']
            # 公司简称
            job_data['companyShortName'] = jobinfo['companyShortName']
            # 公司规模
            job_data['companySize'] = jobinfo['companySize']
            # 工作经验
            job_data['workYear'] = jobinfo['workYear']
            # 学历
            job_data['education'] = jobinfo['education']
            # 公司类型
            job_data['industryField'] = jobinfo['industryField']
            # 职位诱惑
            job_data['positionAdvantage'] = jobinfo['positionAdvantage']
            # 工资
            job_data['salary'] = jobinfo['salary']
            # 公司福利,这个福利因为在数据中键所对应的是list所以我们需要把列表取出来，然后做一个简单的处理
            job_data['fuli'] = ','.join(jobinfo['companyLabelList'])
            # 融资状况
            job_data['financeStage'] = jobinfo['financeStage']
            # 打印出最后的结果
            # print(job_data)
            # 调用存储数据
            save_data(job_data)
        # 判断是否需要发起下一次请求
        # 去除当前页码
        current_page = data['content']['pageNo']
        # 每页返回多少条数据
        page_sise = data['content']['pageSize']
        # 职业总数量
        totalCount = data['content']['positionResult']['totalCount']
        if int(current_page) * page_sise < totalCount:
            # 写一页的页码
            next_page = current_page + 1
            formdata['pn'] = next_page
            print('继续发起请求' + next_page + '页')
            # 本函数的递归调用，因为下个页面所做的事情都一样
            time.sleep(1)
            LaGouSpider(url, formdata)

    else:
        print('请求未成功，稍后再次发送请求')
        time.sleep(10)
        print('重新发起请求'+ str(formdata['pn']) + '页请求')
        LaGouSpider(url, formdata)
def load_data_page(url, formdata):
    """
    请求器
    :param url: 目标url
    :param formdata: 传入的表单输入
    :return:
    """
    user_agent = UserAgent()
    req_header = {
        'User-Agent': user_agent.random,
        'Referer': 'https://www.lagou.com/jobs/list_c%2B%2B?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
    }
    # proxies = {
    #     'http': '59.62.166.126:9999',  # 使用http代理创建http键，值跟代理
    #     'https': '113.105.201.239:3128',  # 使用http代理创建http键，值跟代理
    # }
    # 代理分类
    # 1:免费和收费
    # 2：代理（西刺，快代理，。。。有免费的也有收费的），收费的（阿布云....）
    # handler = request.ProxyHandler(proxies)
    # 自定义opener
    # opener = request.build_opener(handler)
    # 创建request对象
    req = request.Request(url, headers=req_header)
    response = request.urlopen(req)
    # 使用代理
    # response = opener.open(url)
    print(response.status)

    # 将表单数据转为url编码格式的字符串，然后再转为一个bytes类型的数据
    formdata_after = parse.urlencode(formdata).encode('utf-8')
    # 构建一个request对象
    req = request.Request(url, headers=req_header, data=formdata_after)
    response = request.urlopen(req)
    if response.status == 200:
        return response.read().decode('utf-8')


# 存储数据到数据库中
def save_data(jobdata):
    """
    数据存储
    :param jobdata: 是一个字典，存放职位信息
    :return:
    """
    sql = """
        inseRt into lagouwang(%s)
        values(%s)
    """ % (','.join(jobdata.keys()), ','.join(["%s"] * len(jobdata))
           )
    try:
        cursor.execute(sql, list(jobdata.values()))
        mysql_client.commit()
    except Exception as error:
        print(error)
        mysql_client.rollback()


if __name__ == "__main__":
    # 连接数据库
    """
    host=None, 
    user=None, 
    password="",
    database=None, 
    port=0, 
    unix_socket=None,
    charset='',
    """
    mysql_client = pymysql.Connect('localhost', 'root', 'abcdqwe', 'lagouwang', 3306, charset='utf8')
    # 链接数据库的另一种方式
    # db = mysql.connector.connect(user="root", passwd="abcdqwe", database="lagouwang")
    # 创建游标
    cursor = mysql_client.cursor()
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'


    # k_w = input('请输入需要查询的岗位：')
    # start_page = int(input('开始页面'))
    # end_page = int(input('截至页面'))
    # 需要post提交的参数
    formdata = {
        'first': 'true',
        'pn': '1',
        'kd': 'c++'
    }


    LaGouSpider(url, formdata)
