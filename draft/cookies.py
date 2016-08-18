import urllib2
import cookielib


headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}
cookies = cookielib.LWPCookieJar('./cookies.txt')
cookiesHandler = urllib2.HTTPCookieProcessor(cookies)
httpHandler = urllib2.HTTPHandler()
opener = urllib2.build_opener(cookiesHandler)
request = urllib2.Request('http://www.youku.com', headers=headers)
try:
    opener.open(request)
except urllib2.URLError, e:
    print '****************'
cookies.save(ignore_discard = True, ignore_expires = True)
print cookies
