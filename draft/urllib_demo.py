import urllib2

#response = urllib2.urlopen('http://www.zhihu.com')
request = urllib2.Request('http://www.zhihu.com')
response = urllib2.urlopen(request)
print response.geturl()
