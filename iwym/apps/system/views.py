# coding=utf-8
import tushare
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from iwym.apps.data.models import StockBasics, StockHistDailyData

fetch_info = {
    'is_fetching_basic': False,
    'is_fetching_histdata': False,
    'progress_histdata': '0.0%'
}


def index(request):
    return render(request, 'system_index.html')


def fetch_index(request):
    # 暂时从业务表中获取最后同步时间
    basic_sync_time = StockBasics.objects.aggregate(Max('sync_time'))['sync_time__max']
    if basic_sync_time is not None:
        hist_sync_time = StockHistDailyData.objects.aggregate(Max('date'))['date__max']
    return render(request, 'system_fetch_index.html',
                  {'hist_sync_time': hist_sync_time, 'basic_sync_time': basic_sync_time})


def fetch_stock_basic(request):
    result = dict()
    try:
        if fetch_info['is_fetching_basic']:
            result['code'] = '1'
        else:
            fetch_info['is_fetching_basic'] = True
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
                stock.time_to_market = record['timeToMarket']
                stock.sync_time = timezone.now()
                stock.save()
                result['code'] = '0'
                fetch_info['is_fetching_basic'] = False
    except Exception as e:
        result['code'] = '-1'
        result['message'] = e.message
        fetch_info['is_fetching_basic'] = False
    return JsonResponse(result)


def fetch_stock_histdata(request):
    result = dict()
    try:
        if fetch_info['is_fetching_histdata']:
            result['code'] = '1'
        else:
            fetch_info['is_fetching_histdata'] = True
            code = request.POST.get('code')
            start = request.POST.get('start')
            end = request.POST.get('end')
            ktype = request.POST.get('ktype')
            if code is None or len(code) == 0:
                basics = StockBasics.objects.all().order_by('code')
            else:
                basics = StockBasics.objects.get(code=code)
            basics_len = len(basics)
            for i in range(basics_len):
                __fetch_histdata(basics[i], start=start, end=end, ktype=ktype)
                fetch_info['progress_histdata'] = '%.1f%%' % ((i * 100.0) / basics_len)
            result['code'] = '0'
            fetch_info['is_fetching_histdata'] = False
    except Exception as e:
        result['code'] = '-1'
        result['message'] = e.message
        fetch_info['is_fetching_histdata'] = False
    return JsonResponse(result)


def fetch_progress(request):
    return JsonResponse({'code': '0', 'percent': fetch_info['progress_histdata']})


def __fetch_histdata(basic=StockBasics, start=None, end=None, ktype='D'):
    df = tushare.get_hist_data(basic.code, start=start, end=end, ktype=ktype)
    if df is None:
        basic.deal_date = None
        basic.open = None
        basic.close = None
        basic.high = None
        basic.low = None
        basic.volume = None
        basic.price_change = None
        basic.p_change = None
        basic.turnover = None
        basic.save()
    elif df is not None and not df.empty:
        records = df.to_records()
        basic.deal_date = records[-1]['date']
        basic.open = records[-1]['open']
        basic.close = records[-1]['close']
        basic.high = records[-1]['high']
        basic.low = records[-1]['low']
        basic.volume = records[-1]['volume']
        basic.price_change = records[-1]['price_change']
        basic.p_change = records[-1]['p_change']
        basic.turnover = records[-1]['turnover']
        basic.save()
        for record in records:
            data = StockHistDailyData.objects.get_or_create(code=basic.code, date=record['date'])[0]
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
