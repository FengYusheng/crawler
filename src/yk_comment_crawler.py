#-*-coding: utf-8-*-

import urllib
import urllib2
import cookielib
import csv
import re

class YoukuCrawler(object):
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'Referer' : 'www.youku.com'
        }

    def yk_comments_geturl(self, videoid, sid, last_modify, showid = '300647', page = '1'):
        '''
        用户评论页面的url。
        '''
        comments_url = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap='
        comments_url = comments_url + '{"videoid":' + '"' + videoid + '"' + ','
        comments_url = comments_url + '"sid"' + ':' + sid + ','
        comments_url = comments_url + '"last_modify"' + ':' + last_modify + ','
        comments_url = comments_url + '"showid"' + ':' + showid + ','
        comments_url = comments_url + '"chkpgc"' + ':' + '0' + ','
        comments_url = comments_url + '"page"' + ':' + page
        comments_url = comments_url + '}&__ai=&__callback=displayComments'

        return comments_url

    def _yk_get_cookies(self):
        '''
        获取youku的cookies, youku没有设置cookies?
        '''
        cookies = cookielib.MozillaCookieJar('./cookies')
        cookiesHandler = urllib2.HTTPCookieProcessor(cookies)
        opener = urllib2.build_opener(cookiesHandler)
        request = urllib2.Request('http://www.youku.com', headers = self.headers)
        try:
            opener.open(request)
        except urllib2.URLError, e:
            return None
        cookies.save(ignore_discard=True, ignore_expires=True)
        return cookies


    def yk_request(self, comments_url, cookies = None):
        '''
        发送http请求
        '''
        # if cookies is None:
        #     cookies = self._yk_get_cookies()
        #     if cookies is None:
        #         return None
        httpHandler = urllib2.HTTPHandler()
        cookiesHandler = urllib2.HTTPCookieProcessor(cookies)
        opener = urllib2.build_opener(httpHandler)
        url = urllib.quote_plus(comments_url,':/?=~_&')
        request = urllib2.Request(url, headers = self.headers)
        try:
            response = opener.open(request)
        except urllib2.HTTPError, e:
            print 'request %s failed, http status is %d' % (comments_url, e.code)
            return None
        except urllib2.URLError, e:
            print 'request %s faild, reason is %s' % (comments_url, e.reason)
            return None
        else:
            return response


class yk_getCommentsInfo(object):
    '''
    获取用户评论，保存到csv文件中。
    获得用户名，点赞数，评论内容，客户端。
    如何获得subcomments？
    '''

    def yk_commentIsNone(self, comments_page):
        '''
        页面中出现id=\"comment_none\"，说明本金所有评论已经抓取完毕。
        '''
        re_string = r'<div class=\"null\" id=\"comment_none\"><h3>'
        pattern = re.compile(re_string, re.S)
        if re.search(pattern, comments_page):
            return True
        else:
            return False

    def yk_getCommmentsId(self, comments_page):
        '''
        这个方法获得comments id 。
        '''
        pattern = re.compile(r'<div class="comment" id="comment(\d+)">')
        comments_id_list = re.findall(pattern, comments_page)
        return comments_id_list

    def yk_getUsrInfo(self, comments_page, comment_id):
        '''
        根据comment_id，找到用户信息，
        获得的信息包括：用户名，用户特权，用户等级。
        '''
        user_info_dict = {'id':comment_id}
        user_info_id = 'comment_name_' + comment_id
        user_info_name = 'coment_name_' + comment_id
        #获得用户名
        re_string = r'<a href="http:\\/\\/i.youku.com\\/u\\/.+?" target="_blank" id=%s name=%s\s+_hz=.*?>(.+?)<\\/a>' \
                    % (user_info_id, user_info_name)
        pattern = re.compile(re_string)
        user_info = re.search(pattern, comments_page)
        if user_info is None:
            user_info_dict['user_name'] = None
        else:
            user_info_dict['user_name'] = user_info.group(1)

        #获得用户特权信息
        re_string = r'name=%s.+?"http://vip.youku.com/" title="(.+?)"' % user_info_name
        pattern = re.compile(re_string)
        user_info = re.search(pattern, page)
        if user_info is None:
            user_info_dict['user_privilege'] = None
        else:
            user_info_dict['user_privilege'] = user_info.group(1)

        #获得用户等级
        re_string =r'name=%s.+?class="user-grade-icon user-grade-(lv\d+)"' % user_info_name
        pattern = re.compile(re_string)
        user_info = re.search(re_string, page)
        if user_info is None:
            user_info_dict['level'] = None
        else:
            user_info_dict['level'] = user_info.group(1)

        return user_info_dict

    def yk_getUserComment(self, comments_page, comment_id, user_info_dict=None):
        '''
        获得评论内容。
        '''
        re_string = r'<div class="text" id="content_%s" name="content_%s">.+?id="content_.+?">(.+?)<' % (comment_id, comment_id)
        pattern = re.compile(re_string, re.S)
        user_info = re.search(pattern, comments_page)
        return user_info.group(1)

    def yk_getCommentReply(self, comments_page, comment_id, user_info_dict):
        '''
        该评论的点赞数，回复数。
        '''
        #回复数
        re_string = r'<div class="handle" id="reply_%s">.+?data-replynum="(\d+)"' % (comment_id)
        pattern = re.compile(re_string, re.S)
        user_info = re.search(pattern, page)
        user_info_dict['reply_count'] = user_info.group(1)

        #点赞数
        re_string = r'<div class="handle" id="reply_%s">.+?<i class="ico_up"><\\/i>([\s\d]+?)<\\/a>' % (comment_id)
        pattern =re.compile(re_string, re.S)
        user_info = re.search(pattern, page)
        user_info_dict['up_count'] = user_info.group(1)

        #踩楼数
        re_string = r'<div class="handle" id="reply_%s">.+?<i class="ico_down"><\\/i>([\s\d]+?)<\\/a>' % (comment_id)
        pattern = re.compile(re_string, re.S)
        user_info = re.search(pattern, page)
        user_info_dict['down_count'] = user_info.group(1)

        #终端类型
        re_string = r'<div class="handle" id="reply_%s">.+?<em>.+?target="_blank">(.+?)<\\/a>' % comment_id
        pattern = re.compile(re_string, re.S)
        user_info = re.search(pattern, page)
        user_info_dict['client_type'] = user_info.group(1)

if __name__ == '__main__':
    yk_crawler = YoukuCrawler()
    getCommentsTool = yk_getCommentsInfo()
    field_names = ['id', 'user_name', 'user_privilege', 'level',\
                   'reply_count', 'up_count', 'down_count', 'client_type', 'comment', 'url']
    with open('./url_args.csv', 'r') as csv_args_file:
        csvReader = csv.DictReader(csv_args_file)
        for args in csvReader:
            n = 0
            filename = './episode' + args['episode'] + '.csv'
            csv_comments_file = open(filename, 'a')
            csvWriter = csv.DictWriter(csv_comments_file, fieldnames=field_names)
            csvWriter.writeheader()
            while True:
                n += 1
                comment_page_url = yk_crawler.yk_comments_geturl(args['videoid'], args['sid'], args['last_modify'], page = str(n))
                response = yk_crawler.yk_request(comment_page_url)
                if response is None:
                    break
                print response.geturl()
                page = response.read().decode('unicode_escape').encode('utf-8')
                comment_url = response.geturl()

                if getCommentsTool.yk_commentIsNone(page):
                    break

                id_list = getCommentsTool.yk_getCommmentsId(page)
                for comment_id in id_list:
                    user_info_dict = getCommentsTool.yk_getUsrInfo(page, comment_id)
                    user_info_dict['comment'] = getCommentsTool.yk_getUserComment(page, comment_id, user_info_dict)
                    getCommentsTool.yk_getCommentReply(page, comment_id, user_info_dict)
                    user_info_dict['url'] = comment_url
                    csvWriter.writerow(user_info_dict)

            csv_comments_file.close()
