from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from profileUser.views import SignUpView

urlpatterns = [
	url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),

    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('present/', present_page, name='present_page'),

    path('cart/', include('cart.urls')),
	path('profile/', include('profileUser.urls')),
    path('orders/', include('orders.urls')),
    path('', include('shop.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
