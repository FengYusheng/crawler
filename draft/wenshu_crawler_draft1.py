#-*-coding: utf-8-*-

import urllib2
import re
import csv

sbqwenshuPage = 'http://ipr.court.gov.cn/sbqwshz/index.html'

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',

    'Referer':'http://ipr.court.gov.cn/'
}

httpHandler = urllib2.HTTPHandler()
opener = urllib2.build_opener(httpHandler)
request = urllib2.Request(sbqwenshuPage, headers=headers)
response = opener.open(request)
pageContent = response.read()

#pattern = re.compile(r'(?P<link>(?<=<a href="\.\.)/[a-z]+/[a-z]+/\d+/t\d+_\d+\.html(?="))')
#pattern_for_title = re.compile(r'(?<=\.html"\starget="_blank"\stitle=").+(?=">)')
#wenshuPageList = re.findall(pattern, pageContent)
#wenshuPageTitleList = re.findall(pattern_for_title, pageContent)
#print wenshuPageList
#for title in wenshuPageTitleList:
#    print title


pattern = re.compile(r'<a\shref="\.\.(/[a-z]+/[a-z]+/\d+/t\d+_\d+\.html)"\starget="_blank"\stitle="(.+?)">')
wenshuList = re.findall(pattern, pageContent)
with open('wenshu.csv', 'w') as csvFile:
    csvWriter = csv.writer(csvFile)
    for wenshuItem in wenshuList:
        csvWriter.writerow(wenshuItem)
