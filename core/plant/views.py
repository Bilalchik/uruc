import math

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Plant
from .serializers import PlantSerializer
from geopy.distance import great_circle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# api/plant-list/?center_lon=42.815961&center_lat=-74.628320&radius=10000


class PlantListAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('center_lat', openapi.IN_QUERY, description="Широта центра области", type=openapi.TYPE_NUMBER, required=True),
            openapi.Parameter('center_lon', openapi.IN_QUERY, description="Долгота центра области", type=openapi.TYPE_NUMBER, required=True),
            openapi.Parameter('radius', openapi.IN_QUERY, description="Радиус области (в километрах)", type=openapi.TYPE_NUMBER, required=True),
        ],
        responses={
            200: openapi.Response('200 OK', PlantSerializer(many=True)),
            400: "Неверный запрос",
        }
    )
    def get(self, request):

        # Центральные координаты
        center_lat = request.GET.get('center_lat')
        center_lon = request.GET.get('center_lon')

        # Радиус в километрах
        radius = request.GET.get('radius')

        if center_lat is None:
            return Response({"detail": "center_lat is required"}, status=status.HTTP_400_BAD_REQUEST)

        if center_lon is None:
            return Response({"detail": "center_lon is required"}, status=status.HTTP_400_BAD_REQUEST)

        if radius is None:
            return Response({"detail": "radius is required"}, status=status.HTTP_400_BAD_REQUEST)

        center_lat = float(center_lat)
        center_lon = float(center_lon)
        radius = float(radius)

        # Вычисление границ области
        DEGREES_TO_KILOMETERS = 111.32
        min_lat = center_lat - (radius / DEGREES_TO_KILOMETERS)
        max_lat = center_lat + (radius / DEGREES_TO_KILOMETERS)
        min_lon = center_lon - (radius / (DEGREES_TO_KILOMETERS * abs(math.cos(math.radians(center_lat)))))
        max_lon = center_lon + (radius / (DEGREES_TO_KILOMETERS * abs(math.cos(math.radians(center_lat)))))

        plants = Plant.objects.filter(
            location_latitude__range=(min_lat, max_lat),
            location_longitude__range=(min_lon, max_lon)
        )

        serializer = PlantSerializer(plants, many=True)

        return Response(serializer.data)
