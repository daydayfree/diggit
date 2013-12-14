Diggit
===

图片分享社区

![](http://img3.douban.com/view/group_topic/large/public/31629320-1.jpg)


## 搭建开发环境

1. Install virtualenv
> pip install virtualenv  

2. Clone code
> git clone https://github.com/daydayfree/diggit.git  

3. virtualenv
> cd diggit  
> virtualenv venv  
> source venv/bin/activate  

4. Install mongodb
> sudo apt-get install mongodb  

5. Config database
> cp `local_settings.py.tmpl` `local_settings.py`  
> modify `local_settings.py`  

6. Install requirements
> make init-dev  

7. Enjoy :)

## 运行测试用例

> make test  

Mailto: [daydayfree@gmail.com](daydayfree@gmail.com)
