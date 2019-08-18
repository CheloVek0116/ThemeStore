from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreate, name='OrderCreate'),
    path('admin/order/<order_id>/', AdminOrderDetail, name='AdminOrderDetail'),
    path('admin/order/<order_id>/pdf/', AdminOrderPDF, name='AdminOrderPDF'),
    path('', Orders, name='Orders'),
    path('<str:order_id>/', OrderDetail, name='OrderDetail'),


]