import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from opencage.geocoder import OpenCageGeocode
from .models import SearchHistory
from .serializers import SearchHistorySerializer, CitySerializer

WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast'
GEOCODING_API_KEY = '997f5d1d4fbe4a89a6528f98c550a83c' 

class WeatherView(generics.GenericAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

    def get_coordinates(self, city):
        geocoder = OpenCageGeocode(GEOCODING_API_KEY)
        results = geocoder.geocode(city)
        if results and len(results) > 0:
            latitude = results[0]['geometry']['lat']
            longitude = results[0]['geometry']['lng']
            return latitude, longitude
        return None, None

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data['city']

        latitude, longitude = self.get_coordinates(city)
        if latitude is None or longitude is None:
            return Response({'error': 'City not found'}, status=status.HTTP_400_BAD_REQUEST)

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m',
        }

        try:
            response = requests.get(WEATHER_API_URL, params=params)
            response.raise_for_status()  

            data = response.json()

            weather_data = {
                'city': city,
                'temperature': data['hourly']['temperature_2m'][0],  
                'description': 'N/A', 
                'icon': 'N/A',
            }

            search_history, created = SearchHistory.objects.get_or_create(user=request.user, city=city)
            if not created:
                search_history.search_count += 1
                search_history.save()

            return Response(weather_data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': 'Invalid response from weather API'}, status=status.HTTP_400_BAD_REQUEST)



class SearchHistoryView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)
