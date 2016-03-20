from django.conf.urls import url
from iwym.apps.data import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stocks/$', views.stock_index, name='stock_index'),
    url(r'^stocks/(?P<code>[0-9]+)/$', views.stock_detail, name='stock_detail'),
    url(r'^stocks/(?P<code>[0-9]+)/histdata$', views.stock_histdata, name='stock_histdata')
]
