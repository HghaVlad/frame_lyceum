from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class Good(models.Model):

    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Img = models.CharField(max_length=400)
    Price = models.IntegerField()
    Amount = models.IntegerField()
    Bought_col = models.IntegerField(default=0)
    available = models.IntegerField()  # Доступно пользователю или нет 1/0
    Date = models.DateTimeField()  # Дата создания

    def __str__(self):
        return self.Name + " - " + str(self.Amount)


class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Speaker = models.CharField(max_length=50)
    Time = models.CharField(max_length=30)
    Location = models.CharField(max_length=50)
    Places = models.IntegerField()
    Attends = models.IntegerField(default=0)
    available = models.IntegerField(default=0)  # Доступно пользователю или нет 1/0
    Date = models.DateTimeField()  # Дата создания

    def __str__(self):
        return self.Name + " by " + self.Speaker

    def attend(self, user):
        new_reg = Registration()
        new_reg.new("LC", self, user, self.Time)
        new_reg.save()
        self.Attends += 1
        self.save()

    def check_reg(self, user):
        reg = Registration.objects.filter(User=user, Lecture=self).first()
        return reg is None


class Master_class(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Time = ArrayField(ArrayField(models.CharField(max_length=10, blank=True)))
    Location = models.CharField(max_length=50)
    Places = models.IntegerField()
    Attends = models.IntegerField(default=0)
    available = models.IntegerField(default=0)  # Доступно пользователю или нет 1/0
    Date = models.DateTimeField()  # Дата создания

    def __str__(self):
        return self.Name


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


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    Attend_type = models.CharField(max_length=20, choices=[("LC", "Lecture"), ("MS", "Master-class")])
    Lecture = models.ForeignKey(Lecture, null=True, blank=True, on_delete=models.CASCADE)
    Masterclass = models.ForeignKey(Master_class, null=True, blank=True, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Time = models.CharField(max_length=20)
    Registration_time = models.DateTimeField()

    def __str__(self):
        return self.Attend_type + ": " + self.Lecture.Name + " at " + self.Time

    def new(self, attend_type, course, user, time):
        self.Attend_type = attend_type
        self.User = user
        self.Time = time
        self.Registration_time = datetime.now()
        if attend_type == "LC":
            self.Lecture = course
        else:
            self.Masterclass = course

