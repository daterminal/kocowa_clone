from django.urls import path
from django.conf.urls import url,include
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from kocowa.views import UserCreateView, UserCreateDoneTV
from graphene_django.views import GraphQLView
from .schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path('', views.home, name = "home"),
    path('', include('photo.urls')),
    path('',include('weblog.urls')),
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    # path('photo/', include('photo.urls')),
    path('drama/', include('drama.urls')),

    # 인증 URL
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),

    path('mykocowa/',views.mykocowa,name='mykocowa'),
    path('plan/', views.plan, name='plan'),
    # path('getLog/',views.getLog,name='getLog'),
    path('get_client_ip/',views.get_client_ip,name='get_client_ip'),

    path('plan/join_weekly_membership/',views.join_weekly_membership,name='join_weekly_membership'),

    path('checkSubscription/',views.checkSubscription,name='checkSubscription'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
