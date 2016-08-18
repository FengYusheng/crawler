import urllib2
import re

start_url = 'http://ipr.court.gov.cn/'

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

request = urllib2.Request(start_url, headers=headers)
httpHandler = urllib2.HTTPHandler()
opener = urllib2.build_opener(httpHandler)

try:
    response = opener.open(request)
except urllib2.HTTPError, e:
    if hasattr(urllib2.HTTPError, 'code'):
        print e.code
except urllib2.URLError, e:
    if hasattr(urllib2.URLError, 'reason'):
        print e.reason

start_page = response.read()

pattern = re.compile(r'(?<=<a href="./)\D+wshz(?=">)')
wenshuUrlList = re.findall(pattern, start_page)

# for wenshuPage in wenshuUrlList:
#     wenshuPage = start_url + wenshuPage
#     request = urllib2.Request(wenshuPage, headers=headers)
#     response = opener.open(request)
#     print response.geturl()
