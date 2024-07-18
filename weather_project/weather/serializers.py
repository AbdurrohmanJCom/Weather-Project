from rest_framework import serializers
from .models import SearchHistory

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['city', 'search_count', 'last_searched']

class CitySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
