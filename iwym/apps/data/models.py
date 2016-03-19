# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class StockBasics(models.Model):
    code = models.CharField('代码', primary_key=True, null=False, max_length=10)
    name = models.CharField('名称', null=True, max_length=10)
    industry = models.CharField('细分行业', null=True, max_length=20)
    area = models.CharField('地区', null=True, max_length=20)
    pe = models.FloatField('市盈率', null=True)
    outstanding = models.FloatField('流通股本', null=True)
    totals = models.FloatField('总股本(万)', null=True)
    total_assets = models.FloatField('总资产(万)', null=True)
    liquid_assets = models.FloatField('流动资产', null=True)
    fixed_assets = models.FloatField('固定资产', null=True)
    reserved = models.FloatField('公积金', null=True)
    reserved_pershare = models.FloatField('每股公积金', null=True)
    esp = models.FloatField('每股收益', null=True)
    bvps = models.FloatField('每股净资', null=True)
    pb = models.FloatField('市净率', null=True)
    time_to_market = models.DateField('上市日期', null=True)
    sync_time = models.DateTimeField('同步时间', null=True)

    class Meta:
        managed = True
        db_table = 'stock_basics'

    def __str__(self):
        return "{0} ({1})".format(self.name, self.code)


@python_2_unicode_compatible
class StockHistDailyData(models.Model):
    id = models.AutoField('主键', primary_key=True, null=False, blank=False)
    code = models.CharField('代码', null=True, max_length=10)
    date = models.DateField('日期', null=True)
    open = models.FloatField('开盘价', null=True)
    high = models.FloatField('最高价', null=True)
    close = models.FloatField('收盘价', null=True)
    low = models.FloatField('最低价', null=True)
    volume = models.FloatField('成交量', null=True)
    price_change = models.FloatField('价格变动', null=True)
    p_change = models.FloatField('涨跌幅', null=True)
    ma5 = models.FloatField('5均价', null=True)
    ma10 = models.FloatField('10均价', null=True)
    ma20 = models.FloatField('20均价', null=True)
    v_ma5 = models.FloatField('5均量', null=True)
    v_ma10 = models.FloatField('10均量', null=True)
    v_ma20 = models.FloatField('20均量', null=True)
    turnover = models.FloatField('换手率', null=True)

    class Meta:
        managed = True
        db_table = 'stock_hist_daily_data'

    def __str__(self):
        return "{0} ({1})".format(self.code, self.date)
