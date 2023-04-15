from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

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
    path("attend_master_clasees/<int:msclass_id>/<int:time_index>", views.attend_master_class, name="attend_master_class_page"),
    path("master-classes", views.master_classes_page, name="master_classes_page_page"),
    path("get_ms_time", views.get_master_class_time, name="get_master_class_time"),
    path("enter_code", views.enter_code, name="enter_code_page"),
    path("get_code/<str:code>", views.get_code, name="get_code"),
    path("admin_codes", views.admin_code_page, name="admin_code_page"),
    path("admin_code_change/<str:code_name>", views.admin_code_switch, name="admin_code_switch"),
    path("admin_shop", views.admin_shop_page, name="admin_shop_page"),
    path("admin_shop_switch/<int:good_id>", views.admin_shop_swtich, name="admin_shop_switch"),
    path("admin_give_good/<int:order_id>", views.admin_give_good, name="admin_give_good"),
    path("admin_new_code", views.admin_new_code, name="admin_new_code"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
