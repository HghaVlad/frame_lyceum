from django.contrib import admin
from .models import User, Lecture, Good, Master_class, Registration

# Register your models here.
admin.site.register(User)
admin.site.register(Good)
admin.site.register(Lecture)
admin.site.register(Master_class)
admin.site.register(Registration)