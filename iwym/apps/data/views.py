# coding=utf-8

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render

from iwym.apps.data.models import StockBasics, StockHistDailyData


def index(request):
    return render(request, 'data_index.html')


def stock_index(request):
    limit = 15  # 每页显示的记录数
    basics = StockBasics.objects.order_by('code').all()
    paginator = Paginator(basics, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        basics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        basics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        basics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'data_stock_index.html', {'basics': basics})


def stock_detail(request, code):
    basic = StockBasics.objects.get(code=code)
    context = {'basic': basic}
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
