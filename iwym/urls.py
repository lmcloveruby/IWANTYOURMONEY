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
from django.conf.urls import url, include
from django.contrib import admin
from .apps.chart import views as chart_views

urlpatterns = [
    url(r'^data/', include('iwym.apps.data.urls')),
    url(r'^$', chart_views.index),
    url(r'^chart/', chart_views.chart),
    url(r'^chart/data/(\S+)/$', chart_views.get_data),
    url(r'^admin/', admin.site.urls),
]

