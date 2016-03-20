from django.conf.urls import url
from iwym.apps.labs import views


urlpatterns = [
    url(r'^$', views.index, name='labs_index'),
    url(r'^resonate/$', views.resonate_index, name='resonate_index')
]
