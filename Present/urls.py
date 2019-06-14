from django.urls import path
from .views import *

urlpatterns = [
    path("", present_page)
]