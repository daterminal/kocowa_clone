from django.urls import path

from drama import views


app_name = 'drama'
urlpatterns = [

    # Example: /photo/
    path('', views.GenreLV.as_view(), name='index'),

    # Example: /photo/album/, same as /photo/
    path('genre', views.GenreLV.as_view(), name='genre_list'),

    # Example: /photo/album/99/
    path('genre/<int:pk>/', views.GenreDV.as_view(), name='genre_detail'),

    # Example: /photo/photo/99/
    path('drama/<int:pk>/', views.DramaDV.as_view(), name='drama_detail'),

    path('like/', views.likes, name="likes"),

    path('video_detail/<video_key>/', views.video_detail, name='video_detail'),

]

