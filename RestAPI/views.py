# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CityTemperature
from .serializers import WeatherSerializer


# Create your views here.
def index(request, **kwargs):
    return HttpResponse('OK', 'text/plain')


def health(request):
    out = {'status': 'ok'}

    return HttpResponse(json.dumps(out), 'application/json')


class WeatherView(APIView):
    @csrf_exempt
    def get(self, request):
        date = request.query_params.get('date')
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        all_cases = False
        if date:
            temperatures = CityTemperature.objects.filter(date=date)
        elif lat and lon:
            temperatures = CityTemperature.objects.filter(location_lat=lat).filter(location_lon=lon)

        else:
            temperatures = CityTemperature.objects.all()
            all_cases = True

        serializer = WeatherSerializer(temperatures, many=True)
        for data in serializer.data:
            data['temperature'] = map(float, data['temperature'].split(','))
            data['location'] = {"lat": data['location_lat'], "lon": data['location_lon'],
                                "city": data['location_city'], "state": data['location_state']}
            del data['location_lat']
            del data['location_lon']
            del data['location_city']
            del data['location_state']

        if serializer.data:
            return HttpResponse(json.dumps(serializer.data), content_type='application/json', status=200)
        else:
            if all_cases:
                return HttpResponse(json.dumps(serializer.data), content_type='application/json', status=200)
            return HttpResponse(json.dumps(serializer.data), content_type='application/json', status=404)

    @csrf_exempt
    def post(self, request):
        try:
            temperature = request.data
            with transaction.atomic():
                CityTemperature.objects.create(id=temperature['id'],
                                               date=temperature['date'],
                                               temperature=",".join(map(str, temperature['temperature'])),
                                               location_lat=temperature['location']['lat'],
                                               location_lon=temperature['location']['lon'],
                                               location_city=temperature['location']['city'],
                                               location_state=temperature['location']['state'],
                                               )

            return HttpResponse(content_type='application/json', status=201)
        except IntegrityError as ex:
            return HttpResponseBadRequest()
        except Exception as ex:
            return HttpResponseBadRequest()


class WeatherDeleteView(APIView):
    @csrf_exempt
    def delete(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        if start and end and lat and lon:
            CityTemperature.objects.filter(date__gte=start).filter(date__lte=end). \
                filter(location_lat=lat).filter(location_lon=lon).delete()
        else:
            CityTemperature.objects.all().delete()
        return Response()
