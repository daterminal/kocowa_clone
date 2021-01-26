from django.urls import path
from django.conf.urls import url,include
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name = "home"),
    path('admin/', admin.site.urls),
    path('photo/', include('photo.urls')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)