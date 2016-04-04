# -*- coding: UTF-8 -*-
"""iwym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# 项目url命名规则及管理:
# 以app名称作为每个app url的前缀, 每个app目录下都各自管理一个urls.py文件,
# 并在本文件include所有app目录下的url.py文件.

from django.conf.urls import url, include
from django.contrib import admin
from .apps.home import views as home_views

urlpatterns = [
    url(r'^$', home_views.index),
    url(r'^chart/', include('iwym.apps.chart.urls')),
    url(r'^data/', include('iwym.apps.data.urls')),
    url(r'^labs/', include('iwym.apps.labs.urls')),
    url(r'^system/', include('iwym.apps.system.urls')),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^admin/', admin.site.urls),
]
