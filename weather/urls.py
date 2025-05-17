from django.urls import path, include
from weather.views import *

urlpatterns = [
    path('weather/', get_weather, name='get_weather'),

    path('symbols/', SymbolsRateView.as_view(), name='symbols_rate'),

    path('latest/', LatestRateView.as_view(), name='latest_rate'),

]