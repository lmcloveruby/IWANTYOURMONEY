# -*- coding: UTF-8 -*-
import tushare
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from iwym.apps.data.models import StockBasics, StockHistDailyData


def index(request):
    return render(request, 'data_index.html')


def stock_index(request):
    limit = 15  # 每页显示的记录数
    stocks = StockBasics.objects.order_by('code').all()
    paginator = Paginator(stocks, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        stocks = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        stocks = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        stocks = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'data_stock_index.html', {'stocks': stocks})


def stock_detail(request, code):
    stock = StockBasics.objects.get(code=code)
    context = {'stock': stock}
    return render(request, 'data_stock_detail.html', context)


def stock_histdata(request, code):
    stock = StockBasics.objects.filter(code=code)
    if stock.exists():
        data = StockHistDailyData.objects.filter(code=code).order_by('date') \
            .values_list('date', 'open', 'high', 'low', 'close', 'volume')
        if data.exists():
            return JsonResponse({'code': stock[0].code, 'name': stock[0].name,
                                 'data': list(data)}, charset='utf8')
        else:
            return JsonResponse({'code': '1', 'message': '找不到日线数据'}, charset='utf8')
    else:
        return JsonResponse({'code': '1', 'message': 'not found'})


def stock_fetch_basic(request):
    result = dict()
    try:
        df = tushare.get_stock_basics()
        records = df.to_records()
        for record in records:
            stock = StockBasics.objects.get_or_create(code=record['code'])[0]
            stock.name = record['name']
            stock.industry = record['industry']
            stock.area = record['area']
            stock.pe = record['pe']
            stock.outstanding = record['outstanding']
            stock.totals = record['totals']
            stock.total_assets = record['totalAssets']
            stock.liquid_assets = record['liquidAssets']
            stock.fixed_assets = record['fixedAssets']
            stock.reserved = record['reserved']
            stock.reserved_pershare = record['reservedPerShare']
            stock.esp = record['esp']
            stock.bvps = record['bvps']
            stock.pb = record['pb']
            # stock.time_to_market = record['timeToMarket']
            stock.sync_time = timezone.now()
            stock.save()
            result['code'] = '0'
    except Exception as e:
        result['code'] = '1'
        result['message'] = e.message
    return JsonResponse(result)


def stock_fetch_histdata(request):
    result = dict()
    try:
        code = request.GET.get('code')
        df = tushare.get_hist_data(code, start='2016-01-01')
        records = df.to_records()
        for record in records:
            data = StockHistDailyData.objects.get_or_create(code=code, date=record['date'])[0]
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
            result['code'] = '0'
    except Exception as e:
        result['code'] = '1'
        result['message'] = e.message
    return JsonResponse(result)
