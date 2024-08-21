# extractor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('api/keywords/', views.get_keywords, name='get_keywords'),
]
