from django.urls import path
from django.conf.urls import url,include
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from kocowa.views import UserCreateView, UserCreateDoneTV

urlpatterns = [
    # path('', views.home, name = "home"),
    path('', include('photo.urls')),
    path('admin/', admin.site.urls),
    # path('photo/', include('photo.urls')),
    path('drama/', include('drama.urls')),

    # 인증 URL
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),

    path('mykocowa/',views.mykocowa,name='mykocowa'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)