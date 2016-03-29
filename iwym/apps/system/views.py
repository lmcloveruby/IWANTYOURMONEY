# coding=utf-8
import tushare

from anjuke import pinyin
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from iwym.apps.data.models import StockBasics, StockHistDailyData, SjGpJb, SjLshqD, SjLshqW, SjLshqM, SjLshq5, SjLshq15, \
    SjLshq30, SjLshq60
from iwym.libs.utils import str_utils, stock_utils

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
    hist_sync_time = None
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
                code = record['code']
                ggid = stock_utils.gen_ggid(code)
                sj_gp_jb = SjGpJb.objects.get_or_create(ggid=ggid)[0]
                sj_gp_jb.dm = code
                sj_gp_jb.mc = record['name']
                py = pinyin.Converter().convert(record['name'], fmt='fl', sc=False)
                sj_gp_jb.py = str_utils.qj_to_bj(py.lower().replace(' ', ''))
                sj_gp_jb.sshy = record['industry']
                sj_gp_jb.dq = record['area']
                sj_gp_jb.syl = record['pe']
                sj_gp_jb.ltgb = record['outstanding']
                sj_gp_jb.zgb = record['totals']
                sj_gp_jb.zzc = record['totalAssets']
                sj_gp_jb.ldzc = record['liquidAssets']
                sj_gp_jb.gdzc = record['fixedAssets']
                sj_gp_jb.gjj = record['reserved']
                sj_gp_jb.mggj = record['reservedPerShare']
                sj_gp_jb.mgsy = record['esp']
                sj_gp_jb.mgjz = record['bvps']
                sj_gp_jb.sjl = record['pb']
                ssrq = record['timeToMarket']
                if ssrq > 0:
                    sj_gp_jb.ssrq = str_utils.to_timezone(str(ssrq), "%Y%m%d")
                sj_gp_jb.tbsj = timezone.now()
                sj_gp_jb.save()
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
            ggid = request.POST.get('ggid')
            start = request.POST.get('start')
            end = request.POST.get('end')
            ktype = request.POST.get('ktype')
            if ggid is None or len(ggid) == 0:
                basics = SjGpJb.objects.all().order_by('ggid')
            elif len(ggid) == 6:
                basics = SjGpJb.objects.filter(dm=ggid)
            else:
                basics = SjGpJb.objects.filter(ggid=ggid)
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


def __fetch_histdata(basic=SjGpJb, start=None, end=None, ktype='D'):
    df = tushare.get_hist_data(basic.dm, start=start, end=end, ktype=ktype)
    if df is not None and not df.empty:
        records = df.to_records()

        # 接口中date变量在ktype为日, 周, 月时为字符日期, 5, 15, 30, 60时为字符日期时间
        if ktype == 'D' or ktype == 'W' or ktype == 'M':
            pattern = '%Y-%m-%d'
        else:
            pattern = '%Y-%m-%d %H:%M:%S'
        jyrq = str_utils.to_timezone(records[0]['date'], pattern).date()

        # 包含记录且行情日期大于基本表的交易日期，则更新对应字段
        if len(records) > 0 and (basic.jyrq is None or basic.jyrq < jyrq):
            basic.jyrq = records[0]['date']
            basic.kpj = records[0]['open']
            basic.spj = records[0]['close']
            basic.zgj = records[0]['high']
            basic.zdj = records[0]['low']
            basic.cjl = records[0]['volume']
            basic.zde = records[0]['price_change']
            basic.zdf = records[0]['p_change']
            basic.hsl = records[0]['turnover']
            basic.save()
        for record in records:
            model = SjLshqD  # 默认日线
            if ktype == 'W':  # 周线
                model = SjLshqW
            elif ktype == 'M':  # 月线
                model = SjLshqM
            elif ktype == '5':  # 5分线
                model = SjLshq5
            elif ktype == '15':  # 15分线
                model = SjLshq15
            elif ktype == '30':  # 30分线
                model = SjLshq30
            elif ktype == '60':  # 60线
                model = SjLshq60

            sj = str_utils.to_timezone(record['date'], pattern)
            data = model.objects.get_or_create(gpjb=basic, sj=sj)[0]
            data.dm = basic.dm
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
