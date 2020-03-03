from .views import *
from django.urls import path


urlpatterns = [
    path('',  manage_timeline, name='manage_timeline'),
]
