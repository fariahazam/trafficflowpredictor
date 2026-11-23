from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chart.png', views.chart_png, name='chart_png'),
]