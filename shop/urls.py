from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
	path('create/', ProductAdd.as_view(), name='ProductAdd'),
	path('category/<str:category>', ProductList.as_view(), name='ProductList'),
    path('', ProductList.as_view(), name='ProductList'),
    path('<str:username>/<str:slug>/', ProductDetail.as_view(), name='ProductDetail'),
]