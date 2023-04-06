from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .utils import code_generator
# Create your models here.


class Good(models.Model):

    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Img = models.CharField(max_length=400)
    Price = models.IntegerField()
    Quantity = models.IntegerField()  # Количество
    Bought_col = models.IntegerField(default=0)
    available = models.IntegerField()  # Доступно пользователю или нет 1/0
    Date = models.DateTimeField()  # Дата создания

    def __str__(self):
        return str(self.Name) + " - " + str(self.Quantity)

    def purchase(self, user):
        if self.check_user(user):
            new_order = Order()
            new_order.new(self, user)
            self.Bought_col += 1
            user.points -= self.Price
            self.save()
            new_order.save()
            user.save()
            return True

        return False

    def check_user(self, user):
        return Order.objects.filter(User=user, Good=self).count() == 0


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
        return str(self.Name) + " by " + str(self.Speaker)

    def attend(self, user):
        new_reg = Registration()
        new_reg.new("LC", self, user, self.Time)
        new_reg.save()
        self.Attends += 1
        self.save()

    def check_reg(self, user):  # Is available to reg
        return Registration.objects.filter(User=user, Lecture=self).count() == 0


class MasterClass(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Time = ArrayField(ArrayField(models.CharField(max_length=10, blank=True)))
    Location = models.CharField(max_length=50)
    Places = models.IntegerField()
    Attends = ArrayField(ArrayField(models.IntegerField(default=0)))
    available = models.IntegerField(default=0)  # Доступно пользователю или нет 1/0
    Date = models.DateTimeField()  # Дата создания

    def __str__(self):
        return self.Name

    def attend(self, user, time):
        new_reg = Registration()
        new_reg.new("MS", self, user, time)
        new_reg.save()
        for i in range(self.Time.size()):
            if time == self.Time[i]:
                self.Attends[i] += 1
                break
        self.save()

    def check_reg(self, user, time):  # Is available to reg
        return Registration.objects.filter(User=user, Lecture=self, Time=time).count() == 0 and time in self.Time


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
    Master_class = models.ForeignKey(MasterClass, null=True, blank=True, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Time = models.CharField(max_length=20)
    Registration_time = models.DateTimeField()

    def __str__(self):
        return self.Attend_type + ": " + self.Lecture.Name + " at " + self.Time

    def new(self, course_type, course, user, time):
        self.Attend_type = course_type
        self.User = user
        self.Time = time
        self.Registration_time = datetime.now()
        if course_type == "LC":
            self.Lecture = course
        else:
            self.Masterclass = course

    def cancel(self):
        if self.Attend_type == "LC":
            self.Lecture.Attends -= 1
            self.Lecture.save()
        else:
            for i in range(self.Masterclass.Time.size()):
                if self.Time == self.Masterclass.Time[i]:
                    self.Masterclass.Attends[i] += 1
                    self.Masterclass.save()
                    break
        archive = ArchiveRegistration()
        archive.create(self)
        archive.save()
        self.delete()


class ArchiveRegistration(Registration):
    Cancel_time = models.DateTimeField()

    def create(self, data: Registration):
        self.Attend_type = data.Attend_type
        self.Lecture = data.Lecture
        self.Masterclass = data.Masterclass
        self.User = data.User
        self.Time = data.Time
        self.Registration_time = data.Registration_time
        self.Cancel_time = datetime.now()


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    Good = models.ForeignKey(Good, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Price = models.IntegerField()
    Code = models.CharField(max_length=10)
    Status = models.IntegerField(default=0)  # Order status:  0 - Made; 1 - Completed(the good has been taken)
    Made_date = models.DateTimeField()
    Complete_Date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.User.name + ' - ' + self.Good.Name

    def new(self, good, user):
        self.Good = good
        self.User = user
        self.Price = good.Price
        self.Code = code_generator(5)
        self.Made_date = datetime.now()
        self.save()


class ActivationCode(models.Model):
    id = models.AutoField(primary_key=True)
    Amount = models.IntegerField()
    Used = models.IntegerField(default=0)
    Code = models.CharField(max_length=10)
    Available = models.IntegerField(default=1)
    Made_date = models.DateTimeField()

    def make(self, amount):
        self.Amount = amount
        self.Made_date = datetime.now()
        self.Code = code_generator(8)

    def activate(self, user):
        if self.check_user(user):
            self.Used += 1
            new_activation = Activation()
            new_activation.make(self, user)
            user.points += self.Amount
            user.save()
            new_activation.save()
            self.save()
            return True

        return False

    def check_user(self, user):
        return Activation.objects.filter(Code=self, User=user).count() == 0


class Activation(models.Model):
    id = models.AutoField(primary_key=True)
    Code = models.ForeignKey(ActivationCode, default="NONE", on_delete=models.SET_DEFAULT)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Amount = models.IntegerField()
    Date = models.DateTimeField()

    def make(self, code, user):
        self.Code = code
        self.User = user
        self.Amount = code.Amount
        self.Date = datetime.now()

