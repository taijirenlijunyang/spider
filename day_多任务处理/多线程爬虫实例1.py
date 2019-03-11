import queue,json
import requests
import threading
from lxml.html import etree
# 队列的介绍----------------------------------------start
# # maxsize: 指定队列中能存储的最大的数据量
# data_queur = queue.Queue(maxsize=40)
#
# for i in range(50):
#     if not data_queur.full():
#         data_queur.put(i)
# # 判断某个队列是否为空
# isempty = data_queur.empty()
# print(isempty)
#
# # 判断队列是否存满
# isfull = data_queur.full()
# print(isfull)
# # 返回队列的大小
# size = data_queur.qsize()
# print(size)
#
# # 取值
# # FIFO(先进先出)
# print(data_queur.get())
# ------------------------------------------------------end
# 队列是线程之间常用的数据交换形式，因为队列在线程间，是线程安全的
"""
1,创建一个任务队列：存放的是待爬去的url地址
2，创建爬取线程，发起请求，执行任务的下载
3，创建数据队列：存放爬取线程获取的页面源码
4，创建解析进程：解析html源码，提取目标数据，数据持久化
"""
# 获取jobbole的文章列表
# http://blog.jobbole.com/all-posts/1/
# http://blog.jobbole.com/all-posts/page/2/
# http://blog.jobbole.com/all-posts/page/2/
def download_page_data(taskQueue,dataQueue):
    """
    执行下载任务
    :param taskQueue:从任务队列里面取出任务
    :param dataQueue: 将获取到的页面源码存到dataQueue中
    :return:
    """
    while not taskQueue.empty(): # 如果任务队列不为空，我们就取页码，因为队列中拿一个少一个
        page = taskQueue.get()
        print('正在下载第'+str(page)+'页', threading.currentThread().name)
        full_url = 'http://blog.jobbole.com/all-posts/%s/'%str(page)  #拼接完成url链接
        req_header={
            'User-Agent':' Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        response = requests.get(full_url,headers=req_header)  # 发起请求
        if response.status_code == 200:  # 判断是否请求成功
            # 将获取到的页面源码放到dataQueue队列中
            dataQueue.put(response.text)
        else:
            taskQueue.put(page)  # 如果请求失败，重新把page放入任务队列中

def parse_data(dataQueue):
    """
    从dataQueue中去除数据进行解析
    :param dataQueue:
    :return:
    """
    while not dataQueue.empty():
        print('正在解析',threading.currentThread().name)
        html = dataQueue.get()  # 取数据,获取到数据队列中的页面源码
        html_element = etree.HTML(html)
        articles = html_element.xpath('//div[@class="post floated-thumb"]')  # 找到源码中所有文章放置的位置，生成list
        for i in articles:
            data = {}
            # 标题
            data['title'] = i.xpath('.//a[@class="archive-title"]/text()')[0]  # 获取标签
            # 封面
            data['coverImage'] = i.xpath('.//div[@class="post-thumb"]/a/img/@src')[0]
            # 通过页面查看页面我们发现，有的是有评论的，有的没有，所有我们要进行一个判断
            p_a = i.xpath('.//div[@class="post-meta"]/p[1]//a')
            if len(p_a) > 2:
                # tag类型
                data['tag'] = p_a[1].xpath('./text()')[0]
                # 评论量
                data['commentNum'] = p_a[2].xpath('./text()')[0]
            else:
                # tag类型
                data['tag'] = p_a[1].xpath('./text()')[0]
                # 评论量
                data['commentNum'] = '0'  # 如果没有评论量，那么我们给其赋值为0
            # 简介
            data['intro'] = i.xpath('.//span[@class="excerpt"]/p/text()')[0]
            # 时间
            data['publishtime'] = ''.join(i.xpath('.//div[@class="post-meta"]/p[1]/text()'))\
                .replace(' ','').replace('\r','').replace('\n','').replace('.','')

            print(data)
            with open('jobbole.json','a+') as file:
                file.write(json.dumps(data,ensure_ascii=False)+'\n')  # 转为json字符串的形式写入本地

if __name__ == '__main__':
    #c创建一个任务队列
    taskQueue = queue.Queue()
    for i in range(1,200):
        taskQueue.put(i)

    # 创建数据队列
    dataQueue = queue.Queue()

    # 创建线程执行下载任务
    threadName = ['下载线程1号','下载线程2号','下载线程3号','下载线程4号']
    crawl_thread = []
    for name in threadName:
        # 创建线程
        thread_crawl = threading.Thread(target=download_page_data,
                         name=name,
                         args=(taskQueue,dataQueue)
                         )
        crawl_thread.append(thread_crawl)  # 创建一个线程成功后，把它放入列表中，方便同意做join处理
        # 启动线程
        thread_crawl.start()
    # 让所有的爬取线程执行完毕，再回到主线程中继续执行
    for thread in crawl_thread:
        thread.join()

    # 创建解析线程，从dataQueue队列中取出页面源码进行页面源码解析
    threadName = ['解析线程1号', '解析线程2号', '解析线程3号', '解析线程4号']
    parse_thread = []
    for name in threadName:
        thread_parse = threading.Thread(target=parse_data,
                                        name= name,
                                        args=(dataQueue,)
                                        )
        parse_thread.append(thread_parse)
        thread_parse.start()
    for thread in parse_thread:
        thread.join()

    print('完成任务')