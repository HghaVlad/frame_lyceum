from django.shortcuts import render, redirect
from main.models import User, Lecture, Good, MasterClass, Order, ActivationCode, Registration, change_status, change_places

unauthenticated = {"message": "Вы не авторизованы", "comment": "Пожалуйста зарегистрируйтесь"}


# Create your views here.
def admin_code_page(request):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            codes = ActivationCode.objects.all()
            return render(request, "admin_codes.html", {"codes": codes})

    return render(request, "error_page.html", unauthenticated)


def admin_code_switch(request, code_name):  # Change Available
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            code = ActivationCode.objects.filter(Code=code_name).first()
            if code:
                change_status(code)
                return redirect(admin_code_page)
            else:
                return render(request, "error_page.html", {"message": "Код не найден"})

    return render(request, "error_page.html", unauthenticated)


def admin_new_code(request):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            if request.method == "GET":
                return render(request, "admin_new_code.html")
            else:
                new_code = ActivationCode()
                if request.POST["code_points"].isdigit():
                    new_code.make(request.POST['code_points'])
                    new_code.save()
                    return redirect(admin_code_page)

                return render(request, "error_page.html", {"message": "Введите количество баллов целым числом"})

    return render(request, "error_page.html", unauthenticated)


def admin_shop_page(request):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            goods = Good.objects.all()
            orders = Order.objects.all()
            return render(request, "admin_shop.html", {"goods": goods, "orders": orders})

    return render(request, "error_page.html", unauthenticated)


def admin_shop_swtich(request, good_id):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            good = Good.objects.filter(id=good_id).first()
            if good:
                change_status(good)
                return redirect(admin_shop_page)
            else:
                return render(request, "error_page.html", {"message": "Товар не найден"})

    return render(request, "error_page.html", unauthenticated)


def admin_give_good(request, order_id):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            order = Order.objects.filter(id=order_id).first()
            if order:
                order.complete()
                return redirect(admin_shop_page)
            else:
                return render(request, "error_page.html", {"message": "Заказ не найден"})

    return render(request, "error_page.html", unauthenticated)


def admin_users(request):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            users = User.objects.all()
            for user in users:
                lectures = [registration.Lecture for registration in Registration.objects.filter(Attend_type="LC", User=user)]
                master_classes = [registration.Master_class for registration in Registration.objects.filter(Attend_type="MS", User=user)]
                orders = Order.objects.filter(User=user).all()
                user.lectures = lectures
                user.master_classes = master_classes
                user.orders = orders
            return render(request, "admin_users.html", {"users": users})


def admin_courses(request):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            master_classes = MasterClass.objects.all()
            lectures = Lecture.objects.order_by('Order').all()
            return render(request, "admin_courses.html", {"master_classes": master_classes, "lectures": lectures})

    return render(request, "error_page.html", unauthenticated)


def admin_courses_switch(request, course_type, course_id):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            if course_type == "LC":
                lecture = Lecture.objects.filter(id=course_id).first()
                if lecture:
                    change_status(lecture)
                    return redirect(admin_courses)
            elif course_type == "MS":
                master_class = MasterClass.objects.filter(id=course_id).first()
                if master_class:
                    change_status(master_class)
                    return redirect(admin_courses)

            return render(request, "error_page.html", {"message": "Курс не найден"})

    return render(request, "error_page.html", unauthenticated)


def admin_course_change_place(request, course_type, course_id, newplaces):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            if course_type == "LC":
                lecture = Lecture.objects.filter(id=course_id).first()
                if lecture:
                    change_places(lecture, newplaces)
                    return redirect(admin_courses)
            elif course_type == "MS":
                master_class = MasterClass.objects.filter(id=course_id).first()
                if master_class:
                    change_places(master_class, newplaces)
                    return redirect(admin_courses)

            return render(request, "error_page.html", {"message": "Курс не найден"})

    return render(request, "error_page.html", unauthenticated)


def admin_course_registrations(request):
    if request.user.is_authenticated:
        if request.user.Role in ["Admin", 'Manager']:
            registrations = Registration.objects.all()
            return render(request, "admin_registrations.html", {"registrations": registrations})