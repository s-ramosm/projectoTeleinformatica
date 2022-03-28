from .views import data,kappaCategorization
from django.urls import path

urlpatterns = [
    path('data/', data.as_view()),
    path('kappa/', kappaCategorization.as_view())
]