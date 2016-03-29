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
    time_to_market = models.CharField('上市日期', null=True, max_length=10)
    deal_date = models.DateField('交易日期', null=True)
    open = models.FloatField('开盘价', null=True)
    high = models.FloatField('最高价', null=True)
    close = models.FloatField('收盘价', null=True)
    low = models.FloatField('最低价', null=True)
    volume = models.FloatField('成交量', null=True)
    price_change = models.FloatField('价格变动', null=True)
    p_change = models.FloatField('涨跌幅', null=True)
    turnover = models.FloatField('换手率', null=True)
    sync_time = models.DateTimeField('同步时间', null=True)

    class Meta:
        managed = True
        db_table = 'stock_basics'

    def is_raise(self):
        return self.close >= self.open

    def p_change_percent(self):
        return self.p_change * 10

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


# 个股基本信息
@python_2_unicode_compatible
class SjGpJb(models.Model):
    ggid = models.CharField('个股主键', primary_key=True, null=False, max_length=20)
    dm = models.CharField('代码', null=False, max_length=20)
    mc = models.CharField('名称', null=False, max_length=20)
    py = models.CharField('拼音', null=False, max_length=20)
    sshy = models.CharField('所属行业', null=False, max_length=20)
    dq = models.CharField('地区', null=False, max_length=20)
    syl = models.FloatField('市盈率', null=True)
    ltgb = models.FloatField('流通股本（万）', null=True)
    zgb = models.FloatField('总股本（万）', null=True)
    zzc = models.FloatField('总资产（万）', null=True)
    ldzc = models.FloatField('流动资产（万）', null=True)
    gdzc = models.FloatField('固定资产（万）', null=True)
    gjj = models.FloatField('公积金', null=True)
    mggj = models.FloatField('每股公积', null=True)
    mgsy = models.FloatField('每股收益', null=True)
    mgjz = models.FloatField('每股净资', null=True)
    sjl = models.FloatField('市净率', null=True)
    ssrq = models.DateField('上市日期', null=True)
    jyrq = models.DateField('交易日期', null=True)
    zdf = models.FloatField('涨跌幅', null=True)
    zde = models.FloatField('涨跌额', null=True)
    kpj = models.FloatField('开盘价', null=True)
    zgj = models.FloatField('最高价', null=True)
    zdj = models.FloatField('最低价', null=True)
    spj = models.FloatField('收盘价', null=True)
    zsj = models.FloatField('昨收价', null=True)
    hsl = models.FloatField('换手率', null=True)
    cjl = models.FloatField('成交量', null=True)
    cje = models.FloatField('成交额', null=True)
    tbsj = models.DateTimeField('同步时间', null=True)

    class Meta:
        managed = True
        db_table = 'sj_gp_jb'

    def is_raise(self):
        return self.spj >= self.kpj

    def p_change_percent(self):
        return self.hsl * 10

    def __str__(self):
        return "{0} ({1})".format(self.mc, self.dm)


# 历史行情父类
@python_2_unicode_compatible
class _BaseSjLshq(models.Model):
    id = models.AutoField('主键', primary_key=True, null=False, blank=False)
    gpjb = models.ForeignKey(SjGpJb)
    dm = models.CharField('代码', null=False, max_length=20)
    sj = models.DateTimeField('时间', null=True)
    kpj = models.FloatField('开盘价', null=True)
    zgj = models.FloatField('最高价', null=True)
    zdj = models.FloatField('最低价', null=True)
    spj = models.FloatField('收盘价', null=True)
    cjl = models.FloatField('成交量', null=True)
    zde = models.FloatField('涨跌额', null=True)
    zdf = models.FloatField('涨跌幅', null=True)
    jj5 = models.FloatField('5均价', null=True)
    jj10 = models.FloatField('10均价', null=True)
    jj20 = models.FloatField('20均价', null=True)
    jl5 = models.FloatField('5均量', null=True)
    jl10 = models.FloatField('10均量', null=True)
    jl20 = models.FloatField('20均量', null=True)
    hsl = models.FloatField('换手率', null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{0} ({1})".format(self.dm, self.sj)


# 历史行情-5分线
class SjLshq5(_BaseSjLshq):
    class Meta(_BaseSjLshq.Meta):
        managed = True
        db_table = 'sj_lshq_5'


# 历史行情-15分线
class SjLshq15(_BaseSjLshq):
    class Meta(_BaseSjLshq.Meta):
        managed = True
        db_table = 'sj_lshq_15'


# 历史行情-30分线
class SjLshq30(_BaseSjLshq):
    class Meta(_BaseSjLshq.Meta):
        managed = True
        db_table = 'sj_lshq_30'


# 历史行情-60分线
class SjLshq60(_BaseSjLshq):
    class Meta(_BaseSjLshq.Meta):
        managed = True
        db_table = 'sj_lshq_60'


# 历史行情-日线
class SjLshqD(_BaseSjLshq):
    class Meta(_BaseSjLshq.Meta):
        managed = True
        db_table = 'sj_lshq_d'


# 历史行情-周线
class SjLshqW(_BaseSjLshq):
    class Meta(_BaseSjLshq.Meta):
        managed = True
        db_table = 'sj_lshq_w'


# 历史行情-月线
class SjLshqM(_BaseSjLshq):
    class Meta(_BaseSjLshq.Meta):
        managed = True
        db_table = 'sj_lshq_m'


# 研究-共振
@python_2_unicode_compatible
class YjGz(models.Model):
    id = models.AutoField('主键', primary_key=True, null=False, blank=False)
    zt = models.CharField('主题', null=False, max_length=100)
    kssj = models.DateTimeField('开始时间', null=True)
    jssj = models.DateTimeField('结束时间', null=True)

    # 表示以哪一个个股、板块指数或大盘指数作为共振的对照品种
    dzpz = models.CharField('对照品种', null=True, max_length=200)

    # 1、具体的品种
    # 2、品种范围，比如上证的所有股票，则填写：SH%
    # 3、允许品种自由组合，以逗号分隔，比如：个股组合：SH600001,SZ000001,SZ3%,HY%
    yjfw = models.CharField('研究范围', null=True, max_length=200)

    # 取最高价或者收盘价或开盘价
    qzfw = models.CharField('取值类型', null=True, max_length=10)

    pmfw = models.IntegerField('排名范围', null=True)
    sf = models.CharField('算法', null=True, max_length=20)
    clbz = models.CharField('处理标志', null=True, max_length=1)
    cjsj = models.DateTimeField('创建时间', null=True)
    clkssj = models.DateTimeField('处理开始时间', null=True)
    cljssj = models.DateTimeField('处理结束时间', null=True)

    class Meta:
        managed = True
        db_table = 'yj_gz'

    def __str__(self):
        return self.zt


# 研究-共振研究结果
@python_2_unicode_compatible
class YjGzJg(models.Model):
    id = models.AutoField('主键', primary_key=True, null=False, blank=False)
    gpjb = models.ForeignKey(SjGpJb)
    gz = models.ForeignKey(YjGz)
    dm = models.CharField('代码', null=True, max_length=20)
    mc = models.CharField('名称', null=True, max_length=20)
    yjjg = models.CharField('研究结果', null=True, max_length=200)
    pm = models.IntegerField('排名', null=True)

    class Meta:
        managed = True
        db_table = 'yj_gz_jg'

    def __str__(self):
        return "{0} ({1})".format(self.dm, self.mc)
