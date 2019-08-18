from django.urls import path
from .views import *

app_name = 'profileUser'

urlpatterns = [
	path('<str:username>', ProfileDetail.as_view(), name='ProfileDetail'),
	path('<str:username>/cards', ProfileCards.as_view(), name='ProfileCards'),
	path('<str:login_user>/<str:password>/<str:referer>/', LoginRedirect, name='LoginRedirect'),
]