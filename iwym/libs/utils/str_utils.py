# -*- coding: cp936 -*-
from datetime import datetime
from django.utils import timezone


def qj_to_bj(ustring):
    """全角转半角
    :param ustring: 带全角的字符串
    """
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring


def bj_to_qj(ustring):
    """半角转全角
    :param ustring: 带半角的字符串
    """
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring


def to_timezone(date_string, pattern='%Y-%m-%d'):
    """将日期型日期时间转换为django的timezone
    :param date_string: 带半角的字符串
    :param pattern: 格式化匹配符
    """
    return timezone.make_aware(datetime.strptime(date_string, pattern))
