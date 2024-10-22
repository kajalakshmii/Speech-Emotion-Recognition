# SERSapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('predict/', views.predict_emotion, name='predict_emotion'),  # Prediction URL (if needed)
    path('upload-audio/', views.upload_audio, name='upload_audio'),  # Handle audio upload
    path('upload-audio/', views.predict_recorded_audio, name='predict_recorded_audio'),  # For recorded audio

]
