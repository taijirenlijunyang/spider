from urllib import request
from fake_useragent import UserAgent

"""
pener是 urllib.request.OpenerDirector 的实例，我们之前一直都在使用的urlopen，它是一个特殊的opener（也就是模块帮我们构建好的）。

但是基本的urlopen()方法不支持代理、cookie等其他的HTTP/HTTPS高级功能。所以要支持这些功能：

    使用相关的 Handler处理器 来创建特定功能的处理器对象；
    然后通过 urllib.request.build_opener()方法使用这些处理器对象，创建自定义opener对象；
    使用自定义的opener对象，调用open()方法发送请求。

如果程序里所有的请求都使用自定义的opener，可以使用urllib.request.install_opener() 将自定义的 opener 对象 定义为 全局opener，表示如果之后凡是调用urlopen，都将使用这个opener（根据自己的需求来选择）

"""
url = 'https://www.baidu.com'
ua = UserAgent().random

req_header = {
    'User-Agent':ua
}

req = request.Request(url,headers=req_header)

def requset_send(req,timeout=100,context = None):
    """
    自定义请求方法
    :param req: 创建request对象
    :param timeout: 设置超时时间
    :param context: 是否忽略ssl
    handler: 创建这个对象为了实现特定功能
    opener： 为了使用opener.open方法发起请求
    :return:
    """

    if context:
        handler = request.HTTPSHandler(context=context)
        opener = request.build_opener(handler)
        return opener.open(req,timeout=timeout)
    else:
        """
            如果在HTTPHandler()增加debuglevel = 1
            参数，还会将DebugLog打开，
            这样程序在执行的时候，会把收包和发包的报头在屏幕上自动打印出来，方便调试，有时可以省去抓包的工作。
        """
        handler = request.HTTPSHandler(debuglevel=1)
        opener = request.build_opener(handler)
        return opener.open(req, timeout=timeout)

response = requset_send(req)
print(response.status)