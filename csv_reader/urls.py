from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

employee_router = DefaultRouter()
employee_router.register(r'', CheckEmployeeReportView, basename='employeereport')

report_router = DefaultRouter()
report_router.register(r'', ReportView, basename='report')
urlpatterns = [
    path('csv/', CSVReader.as_view(), name='csv_reader'),
    path('employee/', include(employee_router.urls)),
    path('report/', include(report_router.urls)),
]