import csv
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *

# class CSVReader(APIView):
#     def post(self,request):
#         files = request.FILES.getlist('file') if 'file' in request.FILES else [requst.FILES.get('file')]
#
#         if not files:
#             return Response({'message': 'Нужен файл'})
#
#         report = {
#             'employees': [],
#             'summary': {
#                 'total_employees': 0,
#                 'total_hours_worked': 0,
#                 'total_hours_late': 0,
#                 'average_hours_worked': 0,
#                 'average_hourly_rate': 0,
#                 'files_processed': 0,
#                 'files_names': []
#             }
#         }
#
#         processed_files = 0
#         files_names = []
#
#         for file in files:
#             try:
#                 file_content = file.read().decode('utf-8').splitlines()
#                 reader = csv.DictReader(file_content)
#                 processed_files += 1
#                 files_names.append(file.name)
#
#                 for row in reader:
#                     try:
#                         rate_keys = ['hourly_rate', 'rate', 'salary']
#                         for key in rate_keys:
#                             if key in row:
#                                 try:
#                                     hourly_rate_value = int(row[key])
#                                     break
#                                 except (ValueError, TypeError):
#                                     continue
#
#                         employee = {
#                             'employee_id': row['id'],
#                             'name': row.get('name'),
#                             'email': row.get('email'),
#                             'hours_worked': int(row['hours_worked'], 0),
#                             'hourly_rate': hourly_rate_value,
#                             'total_payment': int(row.get('hours_worked', 0)) * hourly_rate_value,
#                             'source_file': file.name
#                         }
#
#                         report['employees'].append(employee)
#
#                         report['summary']['total_employees'] += 1
#                         report['summary']['total_hours_worked'] += int(employee.get('hours_worked', 0))
#                         report['summary']['total_hours_late'] += int(employee.get('hourly_rate', 0))
#
#                         try:
#                             if not EmployeeReport.objects.filter(**employee).exists():
#                                 EmployeeReport.objects.create(**employee)
#                         except Exception as e:
#                             return Response({'error': str(e)})
#                     except (ValueError, KeyError) as e:
#                         continue
#
#             except UnicodeDecodeError:
#                 continue
#             except Exception as e:
#                 continue
#
#         if report['summary']['total_employees'] > 0:
#             report['summary']['average_hours_worked'] = round(
#                 report['summary']['total_hours_worked'] / report['summary']['total_employees'], 2)
#
#             report['summary']['average_hourly_rate'] = round(
#                 report['summary']['total_hours_late'] / report['summary']['total_employees'], 2)
#
#             report['summary']['files_processed'] = processed_files
#             report['summary']['files_names'] = files_names
#
#         if not Report.objects.filter(**report['summary']).exists():
#             Report.objects.create(**report['summary'])
#
#         return Response(report, status=status.HTTP_200_OK)


class CSVReader(APIView):
    RATE_KEYS = ['hourly_rate', 'rate', 'salary']
    REQUIRED_FIELDS = ['id', 'hours_worked']

    def _parse_employee_data(self, row, filename):
        """Парсинг данных сотрудника из строки CSV"""
        employee = {
            'employee_id': int(row['id']),
            'name': row.get('name'),
            'email': row.get('email'),
            'source_file': filename
        }

        employee['hours_worked'] = int(row['hours_worked'])

        employee['hourly_rate'] = self._find_hourly_rate(row)
        employee['total_payment'] = employee['hours_worked'] * employee['hourly_rate']

        return employee

    def _find_hourly_rate(self, row):
        """Поиск значения hourly_rate среди возможных ключей"""
        for key in self.RATE_KEYS:
            if key in row:
                try:
                    return int(row[key])
                except (ValueError, TypeError):
                    continue
        return 0

    def _validate_csv_row(self, row):
        """Проверка обязательных полей"""
        return all(field in row for field in self.REQUIRED_FIELDS)

    def _update_report_summary(self, report, employee):
        """Обновление сводного отчета"""
        report['summary']['total_employees'] += 1
        report['summary']['total_hours_worked'] += employee['hours_worked']
        report['summary']['total_hours_late'] += employee['hourly_rate']

    def _calculate_averages(self, report):
        """Расчет средних значений"""
        if report['summary']['total_employees'] > 0:
            report['summary']['average_hours_worked'] = round(
                report['summary']['total_hours_worked'] / report['summary']['total_employees'], 2)
            report['summary']['average_hourly_rate'] = round(
                report['summary']['total_hours_late'] / report['summary']['total_employees'], 2)

    def _save_employee(self, employee_data):
        """Сохранение сотрудника с проверкой на дубликаты"""
        if not EmployeeReport.objects.filter(**employee_data).exists():
            EmployeeReport.objects.create(**employee_data)

    def _save_report(self, report_data):
        """Сохранение общего отчета"""
        if not Report.objects.filter(**report_data).exists():
            Report.objects.create(**report_data)

    def _init_report(self):
        """Инициализация структуры отчета"""
        return {
            'employees': [],
            'summary': {
                'total_employees': 0,
                'total_hours_worked': 0,
                'total_hours_late': 0,
                'average_hours_worked': 0,
                'average_hourly_rate': 0,
                'files_processed': 0,
                'files_names': []
            }
        }

    def post(self, request):
        files = request.FILES.getlist('file') or []

        if not files:
            return Response(
                {'message': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        report = self._init_report()

        for file in files:
            try:
                if not file.name.endswith('.csv'):
                    return Response({"message": f"Файл {file.name} должен быть формата '.csv' "})

                file_content = file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(file_content)

                report['summary']['files_processed'] += 1
                report['summary']['files_names'].append(file.name)

                for row in reader:
                    if not self._validate_csv_row(row):
                        continue

                    try:
                        employee_data = self._parse_employee_data(row, file.name)
                        report['employees'].append(employee_data)
                        self._update_report_summary(report, employee_data)
                        self._save_employee(employee_data)
                    except (ValueError, KeyError) as e:
                        continue

            except UnicodeDecodeError:
                continue
            except Exception as e:
                continue

        self._calculate_averages(report)
        self._save_report(report['summary'])

        return Response(report, status=status.HTTP_200_OK)


class CheckEmployeeReportView(ModelViewSet):
    http_method_names = ['get', 'options']
    serializer_class = EmployeeReportSerializer
    lookup_field = 'employee_id'
    lookup_url_kwarg = 'employee_id'

    def get_queryset(self):
        return EmployeeReport.objects.all()


class ReportView(ModelViewSet):
    http_method_names = ['get', 'options']
    serializer_class = ReportSerializer

    def get_queryset(self):
        return Report.objects.all()

