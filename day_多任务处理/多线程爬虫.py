import queue
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