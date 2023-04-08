from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User, Lecture, Good, MasterClass, Registration, Order, ActivationCode


# Create your views here.
def index_page(request):
    return render(request, "index.html")


def lecture_page(request):
    lectures = Lecture.objects.filter(available=1).all()
    return render(request, "lectures.html", {"lectures": lectures})


def attend_lecture(request, lecture_id):
    if request.user.is_authenticated:
        my_lecture = Lecture.objects.filter(id=lecture_id).first()
        if my_lecture:
            if my_lecture.Attends < my_lecture.Places:
                if my_lecture.check_reg(request.user):
                    my_lecture.attend(request.user)
                    return render(request, "success_page.html", {"message": "Успех", "comment":
                        "Вы зарегистрировались на лекцию"})
                else:
                    return render(request, "error_page.html", {"message": "Повторная регистрация",
                                                               "comment": "Вы уже зарегистрированы на этой лекции"})
            else:
                return render(request, "error_page.html", {"message": "Нет мест",
                                                           "comment": "К сожалению все свободные места "
                                                                      "на данную лекцию закончились"})
        else:
            return render(request, "error_page.html", {"message": "Лекция не найдена"})

    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста "
                                                                                           "зарегистрируйтесь"})


def master_classes_page(request):
    ms_classes = MasterClass.objects.filter(available=1).all()
    for ms_class in ms_classes:
        ms_class.string_time = [x + " " for x in ms_class.Time]
    return render(request, "master-classes.html", {"master_classes": ms_classes})


def attend_master_class(request, msclass_id, time_index):
    pass


def shop_page(request):
    goods = Good.objects.filter(available=1)
    return render(request, "shop.html", {"goods": goods})


def make_order(request, good_id):
    if request.user.is_authenticated:
        my_good = Good.objects.filter(id=good_id).first()
        if my_good:
            if request.user.points > my_good.Price:
                if my_good.Quantity > my_good.Bought_col:
                    if my_good.purchase(request.user):
                        return render(request, "success_page.html", {"message": "Успех", "comment": "Вы приобрели товар"})
                    else:
                        return render(request, "error_page.html", {"message": "Вы уже приобретали данный товар"})
                else:
                    return render(request, "error_page.html", {"message": "Товар закончился"})
            else:
                return render(request, "error_page.html", {"message": "Недостаточно средств"})
        else:
            return render(request, "error_page.html", {"message": "Товар не найден"})
    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста "
                                                                                           "зарегистрируйтесь"})


def login_page(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        data = request.POST
        user = authenticate(request, username=data['user_login'], password=data['user_password'])
        if user:
            login(request, user)
            return redirect("/")
        return render(request, "login.html", {"status": "Неверный логин или пароль"})


def reg_page(request):
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        data = request.POST
        if data['password'] != data["password_repeat"]:
            return render(request, "reg.html", {"status": "Пароли должны совпадать"})
        elif len(data['password']) < 6:
            return render(request, "reg.html", {"status": "Минимальная длина пароль 6 символов"})
        elif len(data['login']) < 4:
            return render(request, "reg.html", {"status": "Минимальная длина логина 4 символа"})
        else:
            new_user = User()
            new_user.reg(data)
            login(request, new_user)
            return redirect("/")


def logout_page(request):
    logout(request)
    return redirect("/")


def profile_page(request):
    if request.user.is_authenticated:
        lecture_registrations = Registration.objects.filter(User=request.user, Attend_type="LC").all()
        master_class_registrations = Registration.objects.filter(User=request.user, Attend_type="MS").all()
        orders = Order.objects.filter(User=request.user)
        data = {
            "lecture_registrations": lecture_registrations,
            "master_class_registrations": master_class_registrations,
            "orders": orders,
            "user_registrations": len(lecture_registrations) + len(master_class_registrations)
            }
        return render(request, "profile.html", data)


def new_password(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "new_password.html")
        else:
            data = request.POST
            if data['user_password'] != data['user_password_again']:
                return render(request, "new_password.html", {"status": "Пароли должны совпадать"})
            elif len(data['user_password']) < 6:
                return render(request, "new_password.html", {"status": "Минимальная длина пароль 6 символов"})
            else:
                request.user.change_password(data['user_password'])
                return render(request, "success_page.html", {"message": "Успех", "comment": "Вы изменили пароль"})

    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста "
                                                                                           "зарегистрируйтесь"})


def cancel_attend(request, reg_id):
    if request.user.is_authenticated:
        my_reg = Registration.objects.get(id=reg_id, User=request.user)
        if my_reg:
            my_reg.cancel()
            my_reg.delete()
            return redirect("/profile")

        return render(request, "error_page.html", {"message": "Запись не найдена", "comment": "Вы не записаны на "
                                                                                              "данную лекцию"})

    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста "
                                                                                           "зарегистрируйтесь"})


def show_code(request, order_id):
    if request.user.is_authenticated:
        my_oder = Order.objects.filter(id=order_id).first()
        if my_oder:
            return render(request, "show_prise.html", {"order": my_oder})
        else:
            return render(request, "error_page.html", {"message": "Приз не найден"})

    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста "
                                                                                           "зарегистрируйтесь"})


def enter_code(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "enter_code.html")
        else:
            code = request.POST['Code']
            my_activation_code = ActivationCode.objects.filter(Code=code).first()
            if my_activation_code:
                if my_activation_code.activate(request.user):
                    return render(request, "success_page.html", {"message": "Успех", "comment": "Вы активировали код"})
                else:
                    return render(request, "error_page.html", {"message": "Код не найден", "comment": "Вы уже активировали данный QR-код"})
            return render(request, "error_page.html", {"message": "Код не найден", "comment": "Проверьте введенный QR-код"})

    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста "
                                                                                           "зарегистрируйтесь"})


def get_code(request, code):
    if request.user.is_authenticated:
        my_activation_code = ActivationCode.objects.filter(Code=code).first()
        if my_activation_code:
            if my_activation_code.activate(request.user):
                return render(request, "success_page.html", {"message": "Успех", "comment": "Вы активировали код"})
            else:
                return render(request, "error_page.html", {"message": "Код не найден", "comment": "Вы уже активировали данный код"})
        return render(request, "error_page.html", {"message": "Код не найден"})

    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста "
                                                                                           "зарегистрируйтесь"})
