from django.conf.urls import url
from iwym.apps.system import views

urlpatterns = [
    url(r'^$', views.index, name='system_index'),
    url(r'^fetch/$', views.fetch_index, name='fetch_index'),
    url(r'^fetch/stock_basic/$', views.fetch_stock_basic, name='fetch_stock_basic'),
    url(r'^fetch/stock_histdata/$', views.fetch_stock_histdata, name='fetch_stock_histdata'),
    url(r'^fetch/progress/$', views.fetch_progress, name='fetch_progress'),
]
