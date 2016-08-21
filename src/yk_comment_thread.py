#-*-coding: utf-8-*-

import re
import csv
import os.path
import threading


try:
    import urllib.request
except ImportError as e:
    import urllib2
    import urllib

yk_thread_args = threading.local()
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Referer' : 'www.youku.com'
}

field_names = ('id', 'user_name', 'user_privilege', 'level',\
               'reply_count', 'up_count', 'down_count', 'client_type', 'comment', 'url')

class YK_Crawler(object):
    def __init__(self, csvFile):
        self.file = csvFile

    def init(self):
        with open(self.file, 'r') as csv_args_file:
            csvReader = csv.DictReader(csv_args_file)
            for arg in csvReader:
                file_name = 'youku_comments/episode' + arg['episode'] + '.csv'
                if not os.path.exists(file_name):
                    with open(file_name, 'w') as saveFile:
                        csvWriter = csv.DictWriter(saveFile,fieldnames=field_names)
                        csvWriter.writeheader()

    def start(self):
        episode_thread = dict()
        with open(self.file, 'r') as csv_args_file:
            csvReader = csv.DictReader(csv_args_file)
            for arg in csvReader:
                #一集一个线程
                episode_thread[arg['episode']] = ThreadUrl(arg)
                episode_thread[arg['episode']].start()

            for arg in csvReader:
                episode_thread[arg['episode']].join()



class YK_GetCommentsInfo(object):
    '''
    获取用户评论，保存到csv文件中。
    获得用户名，点赞数，评论内容，客户端。
    如何获得subcomments？
    '''

    @staticmethod
    def yk_commentIsNone(comments_page):
        '''
        页面中出现id=\"comment_none\"，说明本集所有评论已经抓取完毕。
        '''
        re_string = r'<div class=\"null\" id=\"comment_none\"><h3>'
        pattern = re.compile(re_string, re.S)
        if re.search(pattern, comments_page):
            return True
        else:
            return False

    @staticmethod
    def yk_getCommmentsId(comments_page):
        '''
        这个方法获得comments id 。
        '''
        pattern = re.compile(r'<div class="comment" id="comment(\d+)">')
        comments_id_list = re.findall(pattern, comments_page)
        return comments_id_list

    @staticmethod
    def yk_getUsrInfo(comments_page, comment_id):
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

    @staticmethod
    def yk_getUserComment(comments_page, comment_id, user_info_dict=None):
        '''
        获得评论内容。
        '''
        re_string = r'<div class="text" id="content_%s" name="content_%s">.+?id="content_.+?">(.+?)<' % (comment_id, comment_id)
        pattern = re.compile(re_string, re.S)
        user_info = re.search(pattern, comments_page)
        return user_info.group(1)

    @staticmethod
    def yk_getCommentReply(comments_page, comment_id, user_info_dict):
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

class YK_Request(object):
    '''
    与发送请求相关的功能
    '''
    @staticmethod
    def yk_request(url):
        response = None
        httpHandler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(httpHandler)
        request = urllib2.Request(url, headers=headers)
        try:
            response = opener.open(request)
        except HTTPError as e:
            print 'http code {0} when access url : {1}'.format(e.code, url)
        except URLError as e:
            print 'error: {0} when access url : {1}'.format(e.reason, url)
        except Exception as e:
            print 'fail to access url : {0}'.format(url)
        finally:
            return response

    @staticmethod
    def yk_getUrl(arg_dict, page = '1'):
        comments_url = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap='
        comments_url = comments_url + '{"videoid":' + '"' + arg_dict['videoid'] + '"' + ','
        comments_url = comments_url + '"sid"' + ':' + arg_dict['sid'] + ','
        comments_url = comments_url + '"last_modify"' + ':' + arg_dict['last_modify'] + ','
        comments_url = comments_url + '"showid"' + ':' + arg_dict['showid'] + ','
        comments_url = comments_url + '"chkpgc"' + ':' + '0' + ','
        comments_url = comments_url + '"page"' + ':' + page
        comments_url = comments_url + '}&__ai=&__callback=displayComments'
        comments_url = urllib.quote_plus(comments_url, ':/?=~_&')

        return comments_url


class ThreadUrl(threading.Thread):
    def __init__(self, arg_dict, func=None):
        super(ThreadUrl, self).__init__()
        self.arg_dict = arg_dict

    def run(self):
        '''
        如果没有指定target参数，thread默认调用run()
        '''
        n = 1
        while True:
            print self.arg_dict['episode'] + ':' + str(n)
            url = YK_Request.yk_getUrl(self.arg_dict, str(n))
            response = YK_Request.yk_request(url)
            if response is None:
                print 'page : {0} and url : {1}'.format(n, url)
                break

            content = response.read().decode('unicode_escape')
            if YK_GetCommentsInfo.yk_commentIsNone(content):
                print 'page : {0} and url : {1}'.format(n, url)
                break

            n += 1

if __name__ == '__main__':
    yk_crawler = YK_Crawler('url_args.csv')
    yk_crawler.init()
    yk_crawler.start()
