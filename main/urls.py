from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("login", views.login_page, name="login_page"),
    path("reg", views.reg_page, name="reg_page"),
    path("profile", views.profile_page, name="profile_page"),
    path("logout", views.logout_page, name="logout_page"),
    path("shop/", views.shop_page, name="shop_page"),
    path("lectures", views.lecture_page, name="lecture_page"),
    path("attend_lectures/<int:lecture_id>", views.attend_lecture, name="attend_lecture_page"),
]
