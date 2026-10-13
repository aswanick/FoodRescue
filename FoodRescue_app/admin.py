from django.contrib import admin

# Register your models here.
from .models import Register , Food, Order



admin.site.register(Register)
admin.site.register(Food)
admin.site.register(Order)