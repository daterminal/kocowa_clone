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
    path('chart3/', views.chart3, name="chart3"),
    path('chartY/', views.chartY, name='chartY'),
    path('chart2Multi/', views.chart2Multi, name='chart2Multi'),
    path('chart2MultiBySex/', views.chart2MultiBySex, name='chart2MultiBySex'),
    path('chartYMulti/', views.chartYMulti, name='chartYMulti'),
    path('chartLikeTop/', views.chartLikeTop, name='chartLikeTop'),
    path('chartmMulti/', views.chartmMulti, name='chartmMulti'),
    path('chartMulti/', views.chartMulti, name='chartMulti'),
]
