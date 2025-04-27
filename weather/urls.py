from django.urls import path, include
from weather.views import get_weather

urlpatterns = [
    path('weather/', get_weather, name='get_weather'),

]