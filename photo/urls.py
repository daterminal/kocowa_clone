from django.urls import path

from photo import views


app_name = 'photo'
urlpatterns = [

    # Example: /photo/
    path('', views.AlbumLV.as_view(), name='index'),

    # Example: /photo/album/, same as /photo/
    path('album', views.AlbumLV.as_view(), name='album_list'),

    # Example: /photo/album/99/
    path('album/<int:pk>/', views.AlbumDV.as_view(), name='album_detail'),

    # Example: /photo/photo/99/
    path('photo/<int:pk>/', views.PhotoDV.as_view(), name='photo_detail'),

    path('love/', views.loves, name="loves"),

    path('photo_video_detail/<video_key>/', views.photo_video_detail, name='photo_video_detail'),

    # path('episode_list/', views.episode_list, name='episode_list'),
]
