from django.shortcuts import render

# Create your views here.

def index_page(request):
    return render(request, "index.html")


def lecture_page(request):
    return render(request, "lectures.html")


def attend_lecture(request, lecture_id):
    pass


def master_classes_page(request):
    return render(request, "master-classes.html")


def attend_master_class(request, msclass_id):
    pass


def shop_page(request):
    return render(request, "shop.html")


def login_page(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        pass


def reg_page(request):
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        pass
