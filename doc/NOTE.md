>　这里记录是我的学习笔记。主要记录一些在实现这个个人作品时学到的一些知识点，主要是关于python开发爬虫用的库的使用


# 里程碑：实现网站的用户登陆
## 需要的知识储备
urllib,urllib2, python对文件的操作。
### `urllib`和`urllib2`
>*如果把页面比作一个人，html就是他的骨架，js就是他的肌肉，css就是他的衣服。*

这两个库经常在在一起使用，`urllib2`用来根据url发送请求，接收响应，`urllib`中的quote方法用来转换url中的特殊字符。

### 盗链vs反盗链
**盗链：**　网站未经同意在自己的页面嵌入别人的站点的连接，如图片，音频，视频。现在发展成一些网站管理者会自己设计爬虫程序，在整个互联网上爬取别人站点上某些资源的连接，放到自己的页面上。*相当于偷邻居家的水电。*

**反盗链:** 随机验证码，uri检查，在图片上加水印，session...

referer字段后面的地址，告诉服务器该请求是从那里来的，服务器检查这个地址是，决定是否允许这个请求。

### 代理
>  python buildopenr 什么语法? http://www.codefrom.com/paper/%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3urllib%E3%80%81urllib2%E5%8F%8Arequests

>  http://www.cnblogs.com/CLTANG/archive/2011/09/15/2178163.html

>  http://blog.csdn.net/pleasecallmewhy/article/details/8924889

### cookie
有些网站会在用户登录后会在本地保存cookie，方便跟踪用户浏览自己网站的历史，对于这种网站爬虫需要先登录，保存cookie，才能爬取网站内容。

cookielib常用来保存cookie，实现模拟登录网站的效果。

### dumptool中的相关例程
*dumptool中的fastquery.py, urlencode.py, urldecode.py*

### 参考资料
[urllib][]
[python I/O][]
[http proxy][]
[lambda][]

[python cartoon][]

[python I/O]:http://www.tutorialspoint.com/python/python_files_io.htm

[urllib]: http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/


[http proxy]: https://imququ.com/post/web-proxy.html

[lambda]: http://www.diveintopython.net/power_of_introspection/lambda_functions.html

[python cartoon]:https://segmentfault.com/q/1010000000179993
