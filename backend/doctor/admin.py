from django.contrib import admin

# Register your models here.
from .models import DoctorModel

admin.site.register(DoctorModel)