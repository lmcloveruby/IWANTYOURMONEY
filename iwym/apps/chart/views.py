# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from iwym.apps.chart.models import StockBasics, HistData


def chart(request):
    return render(request, 'chart.html')


def get_data(request, code):
    basic = StockBasics.objects.filter(code=code)
    if basic.exists():
        data = HistData.objects.filter(code=code).order_by('date')\
            .values_list('date', 'open', 'high', 'low', 'close', 'volume')
        return JsonResponse({'code': basic[0].code, 'name': basic[0].name,
                             'data': list(data)}, charset='utf8')
    else:
        return JsonResponse({'code': '-99999', 'message': 'not found'})