from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import User, Lectures, Goods
# Create your views here.

def index_page(request):
    return render(request, "index.html")


def lecture_page(request):
    lectures = Lectures.objects.filter(available=1).all()
    return render(request, "lectures.html", {"lectures": lectures})


def attend_lecture(request, lecture_id):
    my_lecture = Lectures.objects.filter(id=lecture_id).first()
    if my_lecture is not None:
        pass


def master_classes_page(request):
    return render(request, "master-classes.html")


def attend_master_class(request, msclass_id):
    pass


def shop_page(request):
    goods = Goods.objects.filter(available=1)
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

