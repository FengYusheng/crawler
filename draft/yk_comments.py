#-*-coding: utf-8-*-

'''
unicode_escape：　http://wklken.me/posts/2013/08/31/python-extra-coding-intro.html
'''


import urllib
import urllib2
import re

comments_url = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap=%7B%22videoid%22%3A%22XMTU2MDQ5MTQ5Mg%3D%3D%22%2C%22sid%22%3A957565057%2C%22last_modify%22%3A1469783600%2C%22showid%22%3A300647%2C%22chkpgc%22%3A0%2C%22page%22%3A3%7D&__ai=&__callback=displayComments'
comments_url2 = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap=%7B%22videoid%22%3A%22XMTU2MTYyNTM4NA%3D%3D%22%2C%22sid%22%3A958187092%2C%22last_modify%22%3A1469933101%2C%22showid%22%3A300647%2C%22chkpgc%22%3A0%2C%22page%22%3A144%7D&__ai=&__callback=displayComments'
comments_url3 = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap=%7B%22videoid%22%3A%22XMTU2Mjc4MTAzMg%3D%3D%22%2C%22sid%22%3A958524861%2C%22last_modify%22%3A1469966920%2C%22showid%22%3A300647%2C%22chkpgc%22%3A0%2C%22page%22%3A1%7D&__ai=&__callback=displayComments'
comments_url33 = 'http://comments.youku.com/comments/~ajax/getSubCommentsContent.html?__ap=%7B%22videoid%22%3A390695446%2C%22sid%22%3A%225730024851c3ddb557fc076a%22%2C%22last_modify%22%3A1469975887%2C%22showid%22%3A300647%2C%22chkpgc%22%3A0%2C%22page%22%3A3%7D&__ai=&__callback=VideoComments.subCommentDisplayCallback'
# request = urllib2.Request(comments_url)
# response = urllib2.urlopen(request)
# comments_page = response.read()
# print comments_page.decode('unicode_escape')
# str1 = '\u5267\u60c5\u7684\u77db\u76fe\u6fc0\u5316\u592a\u4e25\u91cd'
# print str1.decode('unicode_escape')

# print urllib.unquote_plus(comments_url)
# print urllib.unquote_plus(comments_url2)
# print urllib.unquote_plus(comments_url22)
# comment_40 = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap={%22videoid%22:%22XMTU2NDE1NTkwNA==%22,%22sid%22:959729414,%22last_modify%22:1470210763,%22showid%22:300647,%22chkpgc%22:0,%22page%22:160}&__ai=&__callback=displayComments'
# request = urllib2.Request(comment_40)
# response = urllib2.urlopen(request)
# page = response.read().decode('unicode_escape')
# re_string = r'<div class=\"null\" id=\"comment_none\"><h3>'
# pattern = re.compile(re_string, re.S)
# result = re.search(pattern, page)
# print result

comment = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap=%7B%22videoid%22%3A%22XMTU2NTA3MDAxMg%3D%3D%22%2C%22sid%22%3A960253813%2C%22last_modify%22%3A1470317490%2C%22showid%22%3A300647%2C%22chkpgc%22%3A0%2C%22page%22%3A1%7D&__ai=&__callback=displayComments'
print urllib.unquote_plus(comment)
