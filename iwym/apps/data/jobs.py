# coding=utf-8
from django_rq import job
from datetime import datetime
from iwym.apps.data.models import SjLshqW, SjGpJb, SjLshqD
import tushare as ts

@job("default")
def fetch_half_hour_data():
    print('-------iwym rq job -------')
    return datetime.now()


"""
每天执行一次, 测试情况,这个方法大概执行了14分钟, 注意停牌股票会不存在交易信息
"""
@job("default")
def fetch_day_data():
    # 需要增加当日是否交易日判断,通联有接口提供
    print('call fetch day\'s job time', datetime.now())
    stocks = SjGpJb.objects.order_by('code').all()
    for basic in stocks:
        print('fetch %s\'s data ' %basic.code)
        df = ts.get_hist_data(basic.code, start=datetime.now().strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'), ktype='D')
        # df = ts.get_hist_data(basic.code, start='2016-04-01', end='2016-04-01', ktype='D')
        if df is not None and not df.empty:
            records = df.to_records()
            # 包含记录且行情日期大于基本表的交易日期，则更新对应字段
            if len(records) > 0 and basic.deal_date < datetime.strptime(records[0]['date'], '%Y-%m-%d').date():
                basic.deal_date = records[0]['date']
                basic.open = records[0]['open']
                basic.close = records[0]['close']
                basic.high = records[0]['high']
                basic.low = records[0]['low']
                basic.volume = records[0]['volume']
                basic.price_change = records[0]['price_change']
                basic.p_change = records[0]['p_change']
                basic.turnover = records[0]['turnover']
                basic.save()
            for record in records:
                data = SjLshqD.objects.get_or_create(code=basic.code, date=record['date'])[0]
                data.open = record['open']
                data.close = record['close']
                data.high = record['high']
                data.low = record['low']
                data.volume = record['volume']
                data.price_change = record['price_change']
                data.p_change = record['p_change']
                data.ma5 = record['ma5']
                data.ma10 = record['ma10']
                data.ma20 = record['ma20']
                data.v_ma5 = record['v_ma5']
                data.v_ma10 = record['v_ma10']
                data.v_ma20 = record['v_ma20']
                data.turnover = record['turnover']
                data.save()


def fetch_week_data():
    print('call fetch week\'s job time', datetime.now())
    stocks = SjGpJb.objects.order_by('code').all()
    for basic in stocks:
        print('fetch %s\'s data ' %basic.code)
        # df = ts.get_hist_data(basic.code, start=datetime.now().strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'), ktype='D')
        df = ts.get_hist_data(basic.code, start='2016-03-28', ktype='w')
        if df is not None and not df.empty:
            records = df.to_records()
            for record in records:
                data = SjLshqW.objects.get_or_create(dm=basic.code, sj=record['date'])[0]
                data.gpjb = basic
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


# 每月执行一次
@job("default")
def fetch_month_data():
    pass
