## IWYM ##

> 一些资源

* [编程零基础应当如何开始学习 Python](https://www.zhihu.com/question/20039623)
* [python基础](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)
* [django教程](http://www.ziqiangxuetang.com/django/django-template2.html) 
* [财经数据包](http://tushare.org/index.html)
* [IDE Pycharm5注册方式](http://www.cnblogs.com/evlon/p/4934705.html)


> 启动方式

* 命令行: python manage.py runserver --settings=iwym.settings.dev[prod][test], dev, prod, test分别代表开发, 生产, 测试环境.
* 使用IDE PyCharm启动: 在启动按钮左侧的下拉列表中选择"Edit Configurations"菜单, 在弹出的对话框中右侧的"Environments variables"输入框, 将"DJANGO_SETTINGS_MODULE=iwym.settings"改为"DJANGO_SETTINGS_MODULE=iwym.settings.dev[prod][test]"