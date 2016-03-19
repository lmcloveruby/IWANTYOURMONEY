# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from datetime import datetime
import tushare as ts
import sys

"""
version 1.0

    运行本文件前请先安装tushare使用环境以及mysql数据
    打开cmd或者terminal输入，切换到该文件所在路径
    输入python data_2_db.py
    用于将tushare数据导入本地mysql数据库
    请根据需要修改config数据库配置
    程序若成功执行，会在本地数据库新建两张表hist_data(历史交易表)和stock_basics(个股信息表),同时插入对应数据
"""
config = {
    'user': 'iwym',
    'password': '123456',
    'host': '127.0.0.1',
    'database': 'iwym',
    'raise_on_warnings': True,
}


# 历史行情数据
def get_hist_data(engine, stock_code):
    df = ts.get_hist_data(stock_code)  # 一次性获取全部日k线数据
    if df is not None:
        df['code'] = stock_code
        df.to_sql('hist_data', engine, if_exists='append')


# 复权历史数据
# 实时行情数据
def get_today_all(engine):
    df = ts.get_today_all()
    df.to_sql('today_all', engine, if_exists='append')


# 历史分笔数据
def get_tick_data(engine, stock_code):
    df = ts.get_tick_data(stock_code, date='2016-03-09')
    df.head(10)
    df.to_sql('tick_data', engine, if_exists='append')


# 当日历史分笔
def get_today_ticks(engine, stock_code):
    df = ts.get_today_ticks(stock_code)
    df.head(10)
    df.to_sql('today_ticks', engine, if_exists='append')


# 实时报价数据 实时分笔
def get_realtime_quote(engine, stock_code):
    df = ts.get_realtime_quotes(stock_code)
    df.to_sql('realtime_quotes', engine, if_exists='append')


# 大盘指数列表
def get_index(engine):
    df = ts.get_index()
    df.to_sql('index', engine, if_exists='append')


# 大单交易数据
def get_sina_big_deal(engine, stock_code):
    df = ts.get_sina_dd(stock_code, date='2016-03-09')  # 默认400手
    df.to_sql('sina_bigdeal', engine, if_exists='append')


# 获得所有个股代码
def get_all_stock_code(engine, condtion='%'):
    return engine.execute('select code from stock_basics where code like %s', condtion)


# 获得全部历史数据
def get_h_data(engine, stock_code, start_condition='2000-01-01'):
    df = ts.get_h_data(stock_code, start=start_condition)  # 一次性获取全部日k线数据
    if df is not None:
        df['code'] = stock_code
        df.to_sql('h_data', engine, if_exists='append')


# 获取个股信息
def get_stock_basics(engine):
    df = ts.get_stock_basics()
    df.to_sql('stock_basics', engine, if_exists='append')


result = ()
db_conn_str = 'mysql://' + config['user'] + ':' + config['password'] + \
              '@' + config['host'] + '/' + config['database'] + '?charset=utf8'

engine = create_engine(db_conn_str)

get_stock_basics(engine)  # 插入个股表

if len(sys.argv) >= 2:
    result = get_all_stock_code(engine, sys.argv[1])
else:
    print('no code condtion，will be input all data data')
    result = get_all_stock_code(engine)

t0 = datetime.now()
for stock in result:
    t1 = datetime.now()
    get_hist_data(engine, stock[0])
    print('input %s\' his_data, use time: %d' % (stock[0], (datetime.now() - t1).seconds))

print('total time used %d seconds' % (datetime.now() - t0).seconds)
