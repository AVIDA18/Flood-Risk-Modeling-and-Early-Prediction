# FPS_Proj/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('predictor.urls')),
]
