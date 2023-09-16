from django.urls import path

from . import views

urlpatterns = [
    path('plant-list/', views.PlantListAPIView.as_view()),
]
