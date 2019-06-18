from django.contrib import admin
from .models import *


@admin.register(CartUser)
class CartUserAdmin(admin.ModelAdmin):
    pass
