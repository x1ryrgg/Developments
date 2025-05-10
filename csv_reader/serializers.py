from rest_framework import serializers

from .models import *


class EmployeeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeReport
        fields = ("employee_id", 'name', 'email', 'hours_worked', 'hourly_rate', 'total_payment', 'source_file', 'created_at')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"