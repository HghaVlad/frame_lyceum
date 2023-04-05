from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User, Lecture, Good
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
                    return render(request, "success_page.html", {"message": "Успех", "comment": "Вы зарегистрировались на лекцию"})
                else:
                    return render(request, "error_page.html", {"message": "Повторная регистрация", "comment": "Вы уже зарегистрированы на этой лекции"})
            else:
                return render(request, "error_page.html", {"message": "Нет мест", "comment": "К сожалению все свободные места на данную лекцию закончились"})
        else:
            return render(request, "error_page.html", {"message": "Лекция не найдена", "comment": "Проверьте ссылку"})

    return render(request, "error_page.html", {"message": "Вы не авторизованы", "comment": "Пожалуйста зарегистрируйтесь"})


def master_classes_page(request):
    return render(request, "master-classes.html")


def attend_master_class(request, msclass_id):
    pass


def shop_page(request):
    goods = Good.objects.filter(available=1)
    return render(request, "shop.html", {"goods": goods})


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
            newuser = User()
            newuser.reg(data)
            login(request, newuser)
            return redirect("/")


def logout_page(request):
    logout(request)
    return redirect("/")


def profile_page(request):
    pass
