from django.contrib import admin

from iwym.apps.data.models import StockBasics, StockHistDailyData


class StockBasicsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'industry', 'area', 'pe', 'outstanding',
                    'totals', 'total_assets', 'liquid_assets', 'fixed_assets',
                    'reserved', 'reserved_pershare', 'esp', 'bvps', 'pb', 'time_to_market')


class StockHistDailyDataAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'open', 'high', 'close', 'low', 'volume',
                    'price_change', 'p_change', 'ma5', 'ma10', 'ma20', 'v_ma5',
                    'v_ma10', 'v_ma20', 'turnover')


admin.site.register(StockBasics, StockBasicsAdmin)
admin.site.register(StockHistDailyData, StockHistDailyDataAdmin)

