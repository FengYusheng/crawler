#-*-coding: utf-8-*-
'''
对于Python2而言，对于一个全局变量，你的函数里如果只使用到了它的值，
而没有对其赋值（指a = XXX这种写法）的话，就不需要声明global。相反，
如果你对其赋了值的话，那么你就需要声明global。声明global的话，
就表示你是在向一个全局变量赋值，而不是在向一个局部变量赋值。

_xsrf、captcha从https://www.zhihu.com获得，表单发送到https://www.zhihu.com/login/email
详细参考: https://github.com/jachinlin/zhihu_spider
'''


import urllib
import urllib2

url = 'https://www.zhihu.com/login/email'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

def login_zhihu():
    global url, headers
    data = {
        'email':'maverick.fengys@gmail.com',
        'password':'159753',
        '_xsrf':'27127445e49290a6a3c010842bcf9320',
        'remember_me':'true'
    }

    data = urllib.urlencode(data)
    print data

    request = urllib2.Request(url, data, headers)
    httpsHandler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(httpsHandler)
    try:
        response = opener.open(request)
    except urllib2.HTTPError, e:
        if hasattr(urllib2.HTTPError, 'code'):
            print e.code
    except urllib2.URLError, e:
        if hasattr(urllib2.URLError, 'reason'):
            print e.reason

    print response.getcode()
    print response.read()

if __name__ == '__main__':
    login_zhihu()
