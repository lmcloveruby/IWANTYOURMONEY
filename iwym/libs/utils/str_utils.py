# -*- coding: cp936 -*-
from datetime import datetime
from django.utils import timezone


def qj_to_bj(ustring):
    """ȫ��ת���
    :param ustring: ��ȫ�ǵ��ַ���
    """
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # ȫ�ǿո�ֱ��ת��
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # ȫ���ַ������ո񣩸��ݹ�ϵת��
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring


def bj_to_qj(ustring):
    """���תȫ��
    :param ustring: ����ǵ��ַ���
    """
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # ��ǿո�ֱ��ת��
            inside_code = 12288
        elif 32 <= inside_code <= 126:  # ����ַ������ո񣩸��ݹ�ϵת��
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring


def to_timezone(date_string, pattern='%Y-%m-%d'):
    """������������ʱ��ת��Ϊdjango��timezone
    :param date_string: ����ǵ��ַ���
    :param pattern: ��ʽ��ƥ���
    """
    return timezone.make_aware(datetime.strptime(date_string, pattern))
