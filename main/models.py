from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Goods(models.Model):
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Img = models.CharField(max_length=400)
    Price = models.IntegerField()
    Amount = models.IntegerField()
    Bought_col = models.IntegerField()
    available = models.IntegerField()  # Доступно пользователю или нет 1/0
    Date = models.DateTimeField()  # Дата создания


class Lectures(models.Model):
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Time = models.CharField(max_length=30)
    Location = models.CharField(max_length=50)
    Places = models.IntegerField()
    Attends = models.IntegerField()
    available = models.IntegerField()  # Доступно пользователю или нет 1/0
    Date = models.DateTimeField()  # Дата создания


# class Master_classes(models.Model, Lectures):
#     pass


class User(AbstractUser):
    name = models.CharField(max_length=100)
    user_class = models.CharField(max_length=20)
    username = models.CharField(max_length=100, unique=True)
    points = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', "user_class"]

    def reg(self, user_data):
        self.name = user_data["user_name"]
        self.user_class = user_data["user_class"]
        self.username = user_data["login"]
        self.save()

