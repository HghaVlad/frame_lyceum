from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("codes", views.admin_code_page, name="admin_code_page"),
    path("code_change/<str:code_name>", views.admin_code_switch, name="admin_code_switch"),
    path("shop", views.admin_shop_page, name="admin_shop_page"),
    path("shop_switch/<int:good_id>", views.admin_shop_swtich, name="admin_shop_switch"),
    path("give_good/<int:order_id>", views.admin_give_good, name="admin_give_good"),
    path("new_code", views.admin_new_code, name="admin_new_code"),
    path("courses", views.admin_courses, name="admin_courses"),
    path("users", views.admin_users, name="admin_users"),
    path("shop_switch/<str:course_type>/<int:course_id>", views.admin_courses_switch, name="admin_courses_switch")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
