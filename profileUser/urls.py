from django.urls import path
from . import views

app_name = 'profileUser'

urlpatterns = [
	path('<str:username>', views.ProfileDetail.as_view(), name='ProfileDetail'),
	path('<str:username>/cards', views.ProfileCards.as_view(), name='ProfileCards'),
]