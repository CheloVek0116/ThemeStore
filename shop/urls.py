from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('<str:username>/<str:slug>/', views.ProductDetail.as_view(), name='ProductDetail'),
    path('category/<str:category>', views.ProductList.as_view(), name='ProductList'),
    path('', views.ProductList.as_view(), name='ProductList'),
]