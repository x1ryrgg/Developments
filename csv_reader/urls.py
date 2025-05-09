from django.urls import path, include
from .views import *

urlpatterns = [
    path('csv/', CSVReader.as_view(), name='csv_reader'),
]