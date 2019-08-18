from rest_framework import serializers

from .models import CityTemperature


class WeatherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    temperature = serializers.CharField(max_length=500)
    date = serializers.DateField()
    location_lat = serializers.FloatField()
    location_lon = serializers.FloatField()
    location_city = serializers.CharField(max_length=50)
    location_state = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return CityTemperature.objects.create(**validated_data)
