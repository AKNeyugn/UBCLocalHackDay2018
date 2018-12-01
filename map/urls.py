from django.conf.urls import include, url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url('^$', views.index, name= 'index'),
]

urlpatterns += staticfiles_urlpatterns()