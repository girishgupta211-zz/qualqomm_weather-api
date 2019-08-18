from django.conf.urls import url
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

from RestAPI.views import health, WeatherView, WeatherDeleteView

urlpatterns = [
    # Dummy route. Can be removed.
    url(r'^/', RedirectView.as_view(url='https://hackerrank.com', permanent=False)),
    url(r'^health', health),
    url(r'^weather', WeatherView.as_view()),
    url(r'^erase', WeatherDeleteView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
