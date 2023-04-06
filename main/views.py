from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User, Lecture, Good, MasterClass, Registration


# Create your views here.
def index_page(request):
    return render(request, "index.html")


def lecture_page(request):
    lectures = Lecture.objects.filter(available=1).all()
    return render(request, "lectures.html", {"lectures": lectures})


def attend_lecture(request, lecture_id):
    if request.user.is_authenticated:
        my_lecture = Lecture.objects.filter(id=lecture_id).first()
        if my_lecture is not None:
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


def attend_master_class(request, msclass_id):
    pass


def shop_page(request):
    goods = Good.objects.filter(available=1)
    return render(request, "shop.html", {"goods": goods})


def make_order(request, good_id):
    if request.user.is_authenticated:
        my_good = Good.objects.filter(id=good_id).first()
        if my_good is not None:
            if request.user.points > my_good.Price:
                if my_good.Quantity > my_good.Bought_col:
                    my_good.purchase(request.user)
                    return render(request, "success_page.html", {"message": "Успех", "comment": "Вы приобрели товар"})
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
        if user is not None:
            login(request, user)
            return redirect("/")
        return render(request, "login.html", {"status": "Неверный логин или пароль"})


def reg_page(request):
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        data = request.POST
        if data['password'] != data["password_repeat"]:
            return render(request, "reg.html", {"status": "Пароль должен совпадать"})
        else:
            new_user = User()
            new_user.reg(data)
            login(request, new_user)
            return redirect("/")


def logout_page(request):
    logout(request)
    return redirect("/")


def profile_page(request):
    registrations = Registration.objects.filter(User=request.user)
    return render(request, "", {"registrations": registrations})


def cancel_attend(request):
    if request.method == "POST":
        data = request.POST
        my_reg = Registration.objects.filter(id=data['reg_id']).first()
        if my_reg is None:
            return render(request, "error_page.html", {"message": "Запись не найдена", "comment": "Вы не записаны на "
                                                                                                  "данную лекцию"})
        else:
            my_reg.cancel()

    return redirect("/profile")
