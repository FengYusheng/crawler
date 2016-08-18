import urllib
import urllib2
import cookielib


url = 'http://www.baidu.com'

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

request = urllib2.Request(url, headers=headers)
cookie = cookielib.MozillaCookieJar(filename='./cookie.txt')
httpsHandler = urllib2.HTTPSHandler()
httpHandler = urllib2.HTTPHandler()
cookieHandler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(cookieHandler)

try:
    response = opener.open(request)
except urllib2.URLError,e:
    print '**********'
    print e.reason

cookie.save(ignore_discard=True, ignore_expires=True)
