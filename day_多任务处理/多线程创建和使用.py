from threading import Thread
import threading
import time

data = []

def download_image(url,num):
    # 下载图片
    global data
    time.sleep(2)
    print(url,num)
    data.append(num)


def read_data():
    global data
    for i in data:
        print(i)

if __name__ == '__main__':

    # 获取当前线程的名称threading.currentThread().name)
    print('主线程开启',threading.currentThread().name)

    # 创建一个子线程
    """
    target=None, : 线程要执行的目标函数
    name=None, ： 创建线程时，指定线程的名称
    args=(),   ：为目标函数，传递参数（元祖类型）
    """
    thread_sub1 = Thread(target=download_image,
                         name='下载线程',
                         args=('http://image.baidu.com/search/detail?ct=503316480&z=0&ipn=d&word=%E7%BE%8E%E5%9B%BE&hs=0&pn=1&spn=0&di=208065730730&pi=0&rn=1&tn=baiduimagedetail&is=0%2C0&ie=utf-8&oe=utf-8&cl=2&lm=-1&cs=1604394911%2C2583311621&os=2472821516%2C4063063283&simid=29599454%2C563549186&adpicid=0&lpn=0&ln=30&fr=ala&fm=&sme=&cg=&bdtype=0&oriquery=&objurl=http%3A%2F%2Fimg0.ph.126.net%2FrCDLXbkA-qpz5-hn1LRa-Q%3D%3D%2F6631979260838506065.jpg&fromurl=ippr_z2C%24qAzdH3FAzdH3Fks52_z%26e3B8mn_z%26e3Bv54AzdH3Fz_z_4tg2_8lnn8d8nAzdH3Fks52AzdH3FfpwptvAzdH3Fdca8cdam0da8m8a8m0cl0mbdAzdH3F&gsm=0&islist=&querylist=',1))
    thread_sub2 = Thread(target=read_data,
                         name='读取线程')
    # 是否开启守护进程(在开启线程之前设置)
    # daemon:False（默认）,在主线程结束的时候会检测，子线程任务是否结束
    # 如果子线程中任务没有完结，则会让子线程正常结束任务
    # daemon：True：在主线程结束的时候会检测，子线程任务是否结束
    # 如果子线程中任务没有完结，则会让子线程跟随主线程一起结束
    # thread_sub1.daemon = True
    # 启动线程
    thread_sub1.start()

    # join():阻塞，等待子线程中的任务执行完毕，再回到主线程中继续执行
    thread_sub1.join()

    # 开启线程
    thread_sub2.start()
    #
    thread_sub2.join()
    print('主线程结束',threading.currentThread().name)
