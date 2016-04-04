# coding=utf-8
from iwym.apps.data.models import SjLshqD, SjGpJb, SjLshqW, SjLshqM
from datetime import datetime
from iwym.libs.utils import str_utils, stock_utils
import tushare as ts
import os
import csv

from iwym.libs.utils import str_utils

"""
数据初始化工具类,注意不要轻易调用,因为需要比较长的时间,比较合理的方式是将所有数据文件保存到本地
通过csv文件初始化数据.
2016-04-02 抓取了所有日线数据,用了3.75小时,总计171w条数据,容量为250m

目前都没有抓取指数数据
"""

# 以下4个方法感觉不适合结构型数据库来存储了,不实现了
def init_5m_data():
    pass


def init_15m_data():
    pass


def init_30m_data():
    pass


def init_hour_data():
    pass

"""
    初始化指数股票基本
"""
def init_zs_gpjb():
    # sh,sz,hs300,sz50,zxb,cyb
    zs = SjGpJb(ggid='SH000001', dm='000001', mc='上证指数')
    zs.save()
    zs = SjGpJb(ggid='SZ399001', dm='399001', mc='深证成指')
    zs.save()
    zs = SjGpJb(ggid='?', dm='?', mc='沪深300') # TODO 待确认
    zs.save()
    zs = SjGpJb(ggid='SH000016', dm='000016', mc='上证50')
    zs.save()
    zs = SjGpJb(ggid='SZ155902', dm='155902', mc='中小板指')
    zs.save()
    zs = SjGpJb(ggid='SZ399006', dm='399006', mc='创业板指')
    zs.save()

"""
    通过数据接口,保存日k线文件到本地
"""
def fetch_day_data2file(start='2016-01-01'):
    stocks = SjGpJb.objects.order_by('dm').all()
    t1 = datetime.now()
    for basic in stocks:
        print('fetch stock: %s\'s data to file' % basic.dm)
        if start is None:
            df = ts.get_hist_data(basic.dm, ktype='D')
        else:
            df = ts.get_hist_data(basic.dm, start=start, ktype='D')

        if df is not None and not df.empty:
            df.to_csv('/Users/lmclinux/code/IWANTYOURMONEY/data-files/%s.csv' %basic.ggid)

    t2 = datetime.now()
    print('init_day_data2file use totaol\' time: %s' % (t2 - t1).total_seconds())


"""
    读取csv文件来实现初始化
    src_path:为csv文件放置目录,约定文件名以股票代码命名
"""
def init_day_data_by_file(import_files_path):
    files = os.listdir(import_files_path)
    for f in files:
        temp_path = import_files_path + '/' + f
        print(temp_path)
        csvfile = file(temp_path, 'rb')
        reader = csv.reader(csvfile)
        reader.next() # 第一行略去
        basic = SjGpJb.objects.get(dm=stock_utils.gen_ggid(f))
        for line in reader:
            print(line)
            sj = str_utils.to_timezone(line[0], '%Y-%m-%d')
            data = SjLshqD.objects.get_or_create(gpjb=basic, sj=sj)[0]
            data.kpj = line[1]
            data.zgj = line[2]
            data.spj = line[3]
            data.zdj = line[4]
            data.cjl = line[5]
            data.zde = line[6]
            data.zdf = line[7]
            data.jj5 = line[8]
            data.jj10 = line[9]
            data.jj20 = line[10]
            data.jl5 = line[11]
            data.jl10 = line[12]
            data.jl20 = line[13]
            data.hsl = line[14]
            data.save()
        csvfile.close()


"""
    抓取日k线数据
    先清空所有数据,再导入,注意目前该方法由于数据过大,会很慢,不要轻易调用(推荐通过init_day_data_by_file方法初始化日k线数据)
"""
def init_day_data(start=None):
    SjLshqD.objects.all().delete()
    stocks = SjGpJb.objects.order_by('dm').all()
    t1 = datetime.now()
    for basic in stocks:
        print('fetch stock: %s\'s data ' % basic.dm)
        if start is None:
            df = ts.get_hist_data(basic.dm, ktype='D')
        else:
            df = ts.get_hist_data(basic.dm, start=start, ktype='D')

        if df is not None and not df.empty:
            records = df.to_records()
            pattern = '%Y-%m-%d'
            for record in records:
                sj = str_utils.to_timezone(record['date'], pattern)
                data = SjLshqD.objects.get_or_create(gpjb=basic, sj=sj)[0]
                data.kpj = record['open']
                data.spj = record['close']
                data.zgj = record['high']
                data.zdj = record['low']
                data.cjl = record['volume']
                data.zde = record['price_change']
                data.zdf = record['p_change']
                data.jj5 = record['ma5']
                data.jj10 = record['ma10']
                data.jj20 = record['ma20']
                data.jl5 = record['v_ma5']
                data.jl10 = record['v_ma10']
                data.jl20 = record['v_ma20']
                data.hsl = record['turnover']
                data.save()

    t2 = datetime.now()
    print('init_day_data use totaol\' time: %s' % (t2 - t1).total_seconds())

"""
    抓取周k线数据
"""
def init_week_data(start=None):
    SjLshqW.objects.all().delete()
    stocks = SjGpJb.objects.order_by('dm').all()
    t1 = datetime.now()
    for basic in stocks:
        print('fetch stock: %s\'s data ' % basic.dm)
        if start is None:
            df = ts.get_hist_data(basic.dm, ktype='W')
        else:
            df = ts.get_hist_data(basic.dm, start=start, ktype='W')

        print(df)
        if df is not None and not df.empty:
            records = df.to_records()
            pattern = '%Y-%m-%d'
            for record in records:
                sj = str_utils.to_timezone(record['date'], pattern)
                data = SjLshqW.objects.get_or_create(gpjb=basic, sj=sj)[0]
                data.kpj = record['open']
                data.spj = record['close']
                data.zgj = record['high']
                data.zdj = record['low']
                data.cjl = record['volume']
                data.zde = record['price_change']
                data.zdf = record['p_change']
                data.jj5 = record['ma5']
                data.jj10 = record['ma10']
                data.jj20 = record['ma20']
                data.jl5 = record['v_ma5']
                data.jl10 = record['v_ma10']
                data.jl20 = record['v_ma20']
                data.hsl = record['turnover']
                data.save()

    t2 = datetime.now()
    print('init_week_data use totaol\' time: %s' % (t2 - t1).total_seconds())


"""
    抓取月k线数据
"""
def init_month_data(start=None):
    SjLshqM.objects.all().delete()
    stocks = SjGpJb.objects.order_by('dm').all()
    t1 = datetime.now()
    for basic in stocks:
        print('fetch stock: %s\'s data ' % basic.dm)
        if start is None:
            df = ts.get_hist_data(basic.dm, ktype='m')
        else:
            df = ts.get_hist_data(basic.dm, start=start, ktype='m')

        print(df)
        if df is not None and not df.empty:
            records = df.to_records()
            pattern = '%Y-%m-%d'
            for record in records:
                sj = str_utils.to_timezone(record['date'], pattern)
                data = SjLshqM.objects.get_or_create(gpjb=basic, sj=sj)[0]
                data.kpj = record['open']
                data.spj = record['close']
                data.zgj = record['high']
                data.zdj = record['low']
                data.cjl = record['volume']
                data.zde = record['price_change']
                data.zdf = record['p_change']
                data.jj5 = record['ma5']
                data.jj10 = record['ma10']
                data.jj20 = record['ma20']
                data.jl5 = record['v_ma5']
                data.jl10 = record['v_ma10']
                data.jl20 = record['v_ma20']
                data.hsl = record['turnover']
                data.save()

    t2 = datetime.now()
    print('init_month_data use totaol\' time: %s' % (t2 - t1).total_seconds())
