from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("login", views.login_page, name="login_page"),
    path("reg", views.reg_page, name="reg_page"),
    path("shop/", views.shop_page, name="shop_page"),
]