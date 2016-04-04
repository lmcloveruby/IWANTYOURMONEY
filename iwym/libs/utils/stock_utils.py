# coding=utf-8
"""股票相关工具函数.
"""


STOCK_TYPE = {
    'SH': 'SH',
    'SZ': 'SZ'
}




def gen_ggid(dm):
    """生成个股主键: 前缀 + dm, 前缀根据代码分为SH(上海)和SZ(上证)
    :param dm: 个股代码
    """

    dm = str(dm)
    if dm.startswith('6'):
        ggid = STOCK_TYPE['SH']
    else:
        ggid = STOCK_TYPE['SZ']
    return ggid + dm
