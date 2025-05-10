from django.db import models


class EmployeeReport(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField()
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    hours_worked = models.IntegerField()
    hourly_rate = models.IntegerField()
    total_payment = models.IntegerField()
    source_file = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.id})"
