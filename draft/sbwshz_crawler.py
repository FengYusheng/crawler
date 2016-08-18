#-*- coding: utf-8-*-

'''
这个脚本只抓取判决文书的title和链接
'''

import urllib2
import csv
import re

host = 'http://ipr.court.gov.cn/'

article_url = set()

class Tool(object):
    '''
    这个类定义了抓取网页中url。
    '''
    def catchWenshuPortalUrl(self, startPage):
        pattern = re.compile(r'(?<=<a href="./)\D+wshz(?=">)')
        wenshuPortalList = re.findall(pattern, startPage)
        return wenshuPortalList

    def catchWenshuArticleUrl(self, wenshuPortal):
        pattern = re.compile(r'(?<=<a href="\.\.)/[a-z]+/[a-z]+/\d+/t\d+_\d+.html(?=")')
        wenshuArticleList = re.findall(pattern, wenshuPortal)
        return wenshuArticleList

    def catchWenshuTitle(self, wenshuPortal):
        '''
        暂时只抓取第一页的title
        '''
        pattern = re.compile(r'(?<=\.html"\starget="_blank"\stitle=").+(?=">)')
        wenshuTitleList = re.findall(pattern, wenshuPortal)
        return wenshuTitleList

    def catchArticle(self, pageContent):
        '''
        抓取文书的title和链接。
        '''
        pattern = re.compile(r'<a\shref="\.\./([a-z]+/[a-z]+/\d+/t\d+_\d+\.html)"\starget="_blank"\stitle="(.+?)">')
        result_list = re.findall(pattern, pageContent)
        return result_list

    def saveTitle(self, title_list, filename):
        '''
        将抓取到底文书title保存到csv文件中
        '''
        with open(filename, 'a') as csvFile:
            csvWriter = csv.writer(csvFile)
            for item in title_list:
                item = list(item)
                item[0] = host + item[0]
                csvWriter.writerow(item)


class Request(object):
    '''
    这个类用来发送http请求。
    '''
    def __init__(self):
        httpHandler = urllib2.HTTPHandler()
        httpsHandler = urllib2.HTTPSHandler()
        self.opener = urllib2.build_opener(httpHandler, httpsHandler)
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                            (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
        }

    def startRequest(self, url, host=None):
        request = urllib2.Request(url, headers=self.headers)
        response = None
        if host:
            request.add_header('Referer','http://ipr.court.gov.cn')
        try:
            response = self.opener.open(request)
        except urllib2.HTTPError, e:
            print str(e.code) + ':' + url
        except urllib2.URLError, e:
            print url + 'fail:' + e.reason
        else:
            return response

if __name__ == '__main__':
    start_url = 'http://ipr.court.gov.cn/sbqwshz/index.html'
    filename = './sbwshz_title.csv'
    request = Request()
    response = request.startRequest(start_url, host)
    if response:
        tool = Tool()
        n = 0
        pageContent = response.read()
        result_list = tool.catchArticle(pageContent)
        tool.saveTitle(result_list, filename)
    while response:
        n += 1
        url = 'http://ipr.court.gov.cn/sbqwshz/index_' + str(n) + '.html'
        response = request.startRequest(url, host)
        if response:
            pageContent = response.read()
            result_list = tool.catchArticle(pageContent)
            tool.saveTitle(result_list, filename)
