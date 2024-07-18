from .views import WeatherView, SearchHistoryView
from django.urls import path


urlpatterns = [
    path('api/weather/', WeatherView.as_view(), name='weather'),
    path('api/history/', SearchHistoryView.as_view(), name='history'),
]
