from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'authorization'
urlpatterns = [
    url(r'^sign_in/$', views.SignIn.as_view(), name='sign_in'),
    url(r'^sign_up/$', views.SignUp.as_view(), name='sign_up'),
    url(r'^sign_out/$', views.SignOut.as_view(), name='sign_out'),
    url(r'^activate/(?P<key>.+)$', views.activation, name='activation'),
]  