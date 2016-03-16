from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class HistData(models.Model):
    code = models.ForeignKey('StockBasics', models.DO_NOTHING, db_column='code', blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    price_change = models.FloatField(blank=True, null=True)
    p_change = models.FloatField(blank=True, null=True)
    ma5 = models.FloatField(blank=True, null=True)
    ma10 = models.FloatField(blank=True, null=True)
    ma20 = models.FloatField(blank=True, null=True)
    v_ma5 = models.FloatField(blank=True, null=True)
    v_ma10 = models.FloatField(blank=True, null=True)
    v_ma20 = models.FloatField(blank=True, null=True)
    turnover = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hist_data'

    def __str__(self):
        return self.code


@python_2_unicode_compatible
class StockBasics(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.TextField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    pe = models.FloatField(blank=True, null=True)
    outstanding = models.FloatField(blank=True, null=True)
    totals = models.FloatField(blank=True, null=True)
    totalassets = models.FloatField(blank=True, null=True)
    liquidassets = models.FloatField(blank=True, null=True)
    fixedassets = models.FloatField(blank=True, null=True)
    reserved = models.FloatField(blank=True, null=True)
    reservedpershare = models.FloatField(blank=True, null=True)
    esp = models.FloatField(blank=True, null=True)
    bvps = models.FloatField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)
    timetomarket = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_basics'

    def __str__(self):
        return "{0} ({1})".format(self.name, self.code)
