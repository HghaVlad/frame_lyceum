from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("login", views.login_page, name="login_page"),
    path("reg", views.reg_page, name="reg_page"),
    path("profile", views.profile_page, name="profile_page"),
    path("show_code/<int:order_id>", views.show_code, name="show_code_page"),
    path("cancel_attend/<int:reg_id>", views.cancel_attend, name="cancel_attend"),
    path("new_password", views.new_password, name="new_password_page"),
    path("logout", views.logout_page, name="logout_page"),
    path("shop/", views.shop_page, name="shop_page"),
    path("make_order/<int:good_id>", views.make_order, name="make_order"),
    path("lectures", views.lecture_page, name="lecture_page"),
    path("attend_lectures/<int:lecture_id>", views.attend_lecture, name="attend_lecture_page"),
    path("enter_code", views.enter_code, name="enter_code_page"),
    path("get_code/<str:code>", views.get_code, name="get_code"),
]
