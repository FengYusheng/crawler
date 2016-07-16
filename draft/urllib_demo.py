import urllib2

#response = urllib2.urlopen('http://www.zhihu.com')
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    }

request = urllib2.Request('https://www.zhihu.com', headers = headers)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
httpHandler = urllib2.HTTPHandler()
opener = urllib2.build_opener(httpHandler, httpsHandler)
#opener.add_handler(httpsHandler)
response = opener.open(request)
#response = urllib2.urlopen(request)
print response.geturl()
