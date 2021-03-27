from django.urls import path

from . import views

urlpatterns = [
    path('chart1/', views.chart, name='chart'),
    path('chart2/', views.chart2, name="chart2"),
]
