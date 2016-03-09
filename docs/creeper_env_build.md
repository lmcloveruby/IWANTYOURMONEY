# 方案一

## 安装python
官网下载合适版本安装（推荐2.7.x版本），windows环境需要配置环境变量，具体参看[这里](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014316090478912dab2a3a9e8f4ed49d28854b292f85bb000)

## 安装easy_install
easy_install为python的第三方包安装工具，具体参看[这里](http://www.cnblogs.com/zhuyp1015/archive/2012/07/17/2596495.html)

## 安装pip
同样用于安装第三方包，具体参看[这里](http://www.tuicool.com/articles/eiM3Er3)

## 搭建TuShare使用环境
1. 安装pandas
2. 安装lxml(pip install lxml)

若遇到pip无法安装lxml(win和mac下都会由于缺少文件无法编译安装)，则通过**easy_install**来安装lxml
> easy_install --allow-hosts=lxml.de,*.python.org lxml==3.4.2

3. 安装tushare(pip install tushare)
4. 确认安装成功,cmd进入python交互，输入，能正常输出则成功安装

> import tushare
> print(tushare.__version__)

## 安装mysql

1. [移步](https://dev.mysql.com/downloads/connector/python/)下载对应版本
2. 参看[这里](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014320107391860b39da6901ed41a296e574ed37104752000)确认安装成功

----------

# 方案二（未尝试）

## 安装[Anaconda](http://www.continuum.io/downloads)包括了Python环境和全部依赖包

## 安装Tushare
类似方案一

## 安装mysql

