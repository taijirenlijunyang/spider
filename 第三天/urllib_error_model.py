# urllib.error：在发起请求过程中，会因为各种情况出现请求异常，从而使代码奔溃所以我们要处理这些异常请求

from urllib import error,request

# URLError:来自urllib库的error模块，继承自OSError,由request模块产生的异常都可以通过捕捉这个类来处理．
#
# 产生的原因主要有：
#
#     没有网络连接
#     服务器连接失败
#     找不到指定的服务器

def check_urlerror():
    """
    异常问题
    1.没有网络
    2.服务器连接失败
    3.找不到指定的服务器
    :return:
    """

    url  = 'https://www.baidux.com/'
    # 异常捕获
    try:
        # response = request.urlopen(url)
        response = request.urlopen(url,timeout=0.01)  # 请求超时timed out
        print(response.status)
    except error.URLError as err:
        print(err.reason)

check_urlerror()

# HTTPError是URLError的子类，我们发出一个请求时，服务器上都会对应一个response应答对象，其中它包含一个数字"响应状态码"。
# 专门用来处理ＨTTP请求错误，比如未认证，页面不存在等
def HttpError():
    url = 'https://www.qidian.com/all/nsacnscn.htm' # 假设url

    try:
        response = request.urlopen(url)
        print(response.status)
    except error.HTTPError as err:
        """   
        有三个属性：
            code:返回HTTP的状态码
            reason:返回错误原因
            headers:返回请求头
        """
        print(err.code)
        print(err.reason)
        print(err.headers)

# HttpError()

# 在实际开发过程中，我们是子类和父类一起使用
# 先判断子类，再判断父类
# 实际开发过程中的写法
"""
    try:
        response = request.urlopen(url)
        print(response.status)
    except error.HTTPError as err:
        
        有三个属性：
            code:返回HTTP的状态码
            reason:返回错误原因
            headers:返回请求头
    
        print(err.code)
        print(err.reason)
        print(err.headers)
    except error.URLError as err:
        print(err.reason)
"""
