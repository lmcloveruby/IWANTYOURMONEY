from django.contrib import admin

from iwym.apps.chart.models import StockBasics, HistData


class StockBasicsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'industry', 'area', 'pe', 'outstanding',
                    'totals', 'totalassets', 'liquidassets', 'fixedassets',
                    'reserved', 'reservedpershare', 'esp', 'bvps', 'pb', 'timetomarket')


class HistDataAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'open', 'high', 'close', 'low', 'volume',
                    'price_change', 'p_change', 'ma5', 'ma10', 'ma20', 'v_ma5',
                    'v_ma10', 'v_ma20', 'turnover')


admin.site.register(StockBasics, StockBasicsAdmin)
admin.site.register(HistData, HistDataAdmin)

