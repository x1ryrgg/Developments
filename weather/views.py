import os

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
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


