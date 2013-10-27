Diggit
===

使用 Tornado 编写的图片分享网站，与 LightBox 类似。
![](http://img3.douban.com/view/group_topic/large/public/31629320-1.jpg)


Requirement
===
+ pymongo
+ tornado
+ mmseg

Nginx
===
图片上传时使用了 Nginx Upload Module 上传模块，可以在 Nginx 配置文件中设置文件上传之后提交到哪个 View 来处理。
提交的时候会另外提交几个图片相关的参数，Nginx 会传递给 View 图片的大小，路径，MD5值，如果你还想要其他的值，
可以在 Nginx 配置文件中设置。

具体上传的文档可以参考[这里](http://www.grid.net.ru/nginx/upload.en.html)
上面有 Demo，感兴趣的同学可以尝试一下。


Mailto: [daydayfree@gmail.com](daydayfree@gmail.com)
