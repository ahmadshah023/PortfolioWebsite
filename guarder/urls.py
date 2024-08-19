from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('code', views.code, name='code'),
    path('qr-code',views.qrcode_view , name='qrcode'),
    path('barcode', views.barcode_view, name='barcode'),
    path('url-shorten', views.URLshorten, name='url-shorten')
]
