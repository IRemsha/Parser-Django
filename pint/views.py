from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ad
from .filters import *
from .serializers import *
from rest_framework import generics


class AllView(APIView):
    def get(self, request, offset, amount):
        result = Ad.objects.all()[offset:offset+amount]
        clean_data = []
        for row in result:
            clean_data.append(AdSerializer(row).data)
        return Response(clean_data)


class FilterView(generics.ListAPIView):
    queryset = Ad.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdFilter
    serializer_class = AdSerializer
