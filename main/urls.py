from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.Main.as_view(), name='main'),
    url(r'^search/(?P<search_str>[^\s]+)/$', views.SearchPage.as_view(), name='search'),
    url(r'^post_page/(?P<post_id>[0-9]+)/$', views.PostPage.as_view(), name='post_page'),
]  