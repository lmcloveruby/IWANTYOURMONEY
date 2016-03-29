# coding=utf-8

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render

from iwym.apps.data.models import StockBasics, StockHistDailyData, SjGpJb, SjLshqD


def index(request):
    return render(request, 'data_index.html')


def stock_index(request):
    limit = 15  # 每页显示的记录数
    datas = SjGpJb.objects.order_by('dm').all()
    paginator = Paginator(datas, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        datas = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        datas = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        datas = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'data_stock_index.html', {'datas': datas})


def stock_detail(request, ggid):
    data = SjGpJb.objects.get(ggid=ggid)
    context = {'data': data}
    return render(request, 'data_stock_detail.html', context)


def stock_histdata(request, ggid):
    stock = SjGpJb.objects.filter(ggid=ggid)
    if stock.exists():
        # 时间,开盘价^最高价^最低价^收盘价^成交量^成交额^涨跌幅^换手率^五日均线^十日均线^20日均线^30日均线^昨日收盘价 ^当前点离左边的相对距离
        data = SjLshqD.objects.filter(gpjb=stock).order_by('sj')\
            .values_list('sj', 'kpj', 'zgj', 'zdj', 'spj', 'cjl',
                         'zde', 'zdf', 'hsl', 'jj5', 'jj10', 'jj20')
        if data.exists():
            return JsonResponse({'code': stock[0].dm, 'name': stock[0].mc,
                                 'data': list(data)}, charset='utf8')
        else:
            return JsonResponse({'code': '1', 'message': '找不到日线数据'}, charset='utf8')
    else:
        return JsonResponse({'code': '1', 'message': 'not found'})
