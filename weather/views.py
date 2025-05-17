import os
from urllib import response
import datetime

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = '088cf94d4eca6f9599eb368cbdb3bd26' #os.getenv('OPENWEATHERMAP_API_KEY')


@api_view(['GET'])
def get_weather(request):
    city_name = request.query_params.get('city')
    if not city_name:
        return Response({'error': 'City parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return Response({'error': data.get('message', 'Failed to fetch weather data')},
                            status=response.status_code)


        pressure_hpa = data['main']['pressure']
        pressure_mmhg = round(pressure_hpa * 0.750062, 2)

        weather_data = {
            'city': data['name'],
            'temperature': f"{data['main']['temp']} °C",
            'pressure': f"{pressure_mmhg} мм рт.ст.",
            'wind_speed': f"{data['wind']['speed']} м/с",
        }

        return Response(weather_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SymbolsRateView(APIView):
    def get(self,request):
        url = "https://data.fixer.io/api/symbols?access_key=8fd2adec91e2983adf9f30d29bbe3a9f"
        symbol = request.query_params.get('symbol')

        response = requests.get(url)
        data = response.json()
        # dollar = {key: value for key, value in data['symbols'].items() if "Dollar" in value}

        if symbol:
            if symbol in data['symbols']:
                return Response({symbol: data['symbols'][symbol]}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Symbol not found"}, status=404)
        else:
            return Response(data['symbols'])



class LatestRateView(APIView):
    def get(self,request):
        url = 'https://data.fixer.io/api/latest?access_key=8fd2adec91e2983adf9f30d29bbe3a9f'

        response = requests.get(url)
        data = response.json()

        return Response(data)