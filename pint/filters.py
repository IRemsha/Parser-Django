from .models import *
from django_filters import rest_framework as filters


class AdFilter(filters.FilterSet):
    class Meta:
        model = Ad
        fields = {
            'price': ['lt', 'gt'],
            'city': [],
            'room': ['lt', 'gt'],
            'floor': ['lt', 'gt'],
            'square_all': ['lt', 'gt'],
            'square_kitchen': ['lt', 'gt'],
            'square_live': ['lt', 'gt']
        }
