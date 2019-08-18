from django.contrib import admin
from .models import *



@admin.register(Order, OrderItem)
class OrderAdmin(admin.ModelAdmin):
    pass
