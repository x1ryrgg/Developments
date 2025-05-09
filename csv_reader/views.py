import csv
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class CSVReader(APIView):
    def post(self,request):
        file = request.FILES.get('file')

        if not file:
            return Response({'message': 'Нужен файл'})

        report = {
            'employees': [],
            'summary': {
                'total_employees': 0,
                'total_hours_worked': 0,
                'total_hourly_rate': 0,
                'average_hours_worked': 0,
                'average_hourly_rate': 0
            }
        }

        try:
            file_content = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(file_content)

            for row in reader:
                try:
                    employee = {
                        'id': row['id'],
                        'name': row.get('name'),
                        'email': row.get('email'),
                        'hours_worked': row['hours_worked'],
                        'hourly_rate': int(row.get('hourly_rate', 0)),
                        'total_payment': int(row.get('hours_worked', 0)) * int(row.get('hourly_rate', 0))
                    }

                    report['employees'].append(employee)

                    report['summary']['total_employees'] += 1
                    report['summary']['total_hours_worked'] += int(employee.get('hours_worked', 0))
                    report['summary']['total_hours_late'] += int(employee.get('hourly_rate', 0))
                except (ValueError, KeyError) as e:
                    continue

            if report['summary']['total_employees'] > 0:
                report['summary']['average_hours_worked'] = round(
                    report['summary']['total_hours_worked'] / report['summary']['total_employees'],
                    2
                )
                report['summary']['average_hourly_rate'] = round(
                    report['summary']['total_hourly_rate'] / report['summary']['total_employees'],
                    2
                )

            return Response(report, status=status.HTTP_200_OK)

        except Exception as e:
            return Response("Ошибка с обработкой файла:  " + str(e))