from django.contrib import admin
from .models import User, Lecture, Good, MasterClass, Registration, Order, Activation, ActivationCode

# Register your models here.
admin.site.register(User)
admin.site.register(Good)
admin.site.register(Lecture)
admin.site.register(MasterClass)
admin.site.register(Registration)
admin.site.register(Order)
admin.site.register(ActivationCode)
admin.site.register(Activation)
