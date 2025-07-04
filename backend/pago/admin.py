from django.contrib import admin

# Register your models here.
from .models import BilleteraModel, FormaPagoModel, TransaccionModel

admin.site.register(BilleteraModel)
admin.site.register(FormaPagoModel)
admin.site.register(TransaccionModel)