from django.urls import path

from . import views

urlpatterns = [
    path('chart1/', views.chart, name='chart'),
    path('chart2/', views.chart2, name="chart2"),
    path('chart2/bySex/', views.chart2bySex, name="chart2bySex"),
    path('chart2/byAge/', views.chart2byAge, name="chart2byAge"),
    path('chart2/byCity/', views.chart2byCity, name="chart2byCity"),
    path('chartM/', views.chartM, name="chartM"),
    path('chartM/bySex/', views.chartM_Sex, name="chartM_Sex"),
    path('chartM/byAge/', views.chartM_Age, name="chartM_Age"),
    path('chartM/byCity/', views.chartM_City, name="chartM_City"),
]
