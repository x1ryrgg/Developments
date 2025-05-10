import csv
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *

class CSVReader(APIView):
    def post(self,request):
        files = request.FILES.getlist('file') if 'file' in request.FILES else [requst.FILES.get('file')]

        if not files:
            return Response({'message': 'Нужен файл'})

        report = {
            'employees': [],
            'summary': {
                'total_employees': 0,
                'total_hours_worked': 0,
                'total_hours_late': 0,
                'average_hours_worked': 0,
                'average_hourly_rate': 0,
                'files_processed': 0
            }
        }

        processed_files = 0

        for file in files:
            try:
                file_content = file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(file_content)
                processed_files += 1

                for row in reader:
                    try:
                        rate_keys = ['hourly_rate', 'rate', 'salary']
                        for key in rate_keys:
                            if key in row:
                                try:
                                    hourly_rate_value = int(row[key])
                                    break
                                except (ValueError, TypeError):
                                    continue

                        employee = {
                            'employee_id': row['id'],
                            'name': row.get('name'),
                            'email': row.get('email'),
                            'hours_worked': int(row['hours_worked'], 0),
                            'hourly_rate': hourly_rate_value,
                            'total_payment': int(row.get('hours_worked', 0)) * hourly_rate_value,
                            'source_file': file.name
                        }

                        report['employees'].append(employee)

                        report['summary']['total_employees'] += 1
                        report['summary']['total_hours_worked'] += int(employee.get('hours_worked', 0))
                        report['summary']['total_hours_late'] += int(employee.get('hourly_rate', 0))

                        try:
                            if not EmployeeReport.objects.filter(**employee).exists():
                                EmployeeReport.objects.create(**employee)
                        except Exception as e:
                            return Response({'error': str(e)})
                    except (ValueError, KeyError) as e:
                        continue

            except UnicodeDecodeError:
                continue
            except Exception as e:
                continue

        if report['summary']['total_employees'] > 0:
            report['summary']['average_hours_worked'] = round(
                report['summary']['total_hours_worked'] / report['summary']['total_employees'], 2)

            report['summary']['average_hourly_rate'] = round(
                report['summary']['total_hours_late'] / report['summary']['total_employees'], 2)

            report['summary']['files_processed'] = processed_files

        return Response(report, status=status.HTTP_200_OK)
