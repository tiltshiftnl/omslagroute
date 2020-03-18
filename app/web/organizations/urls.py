from .views import *
from django.urls import path


urlpatterns = [
    path('',  manage_organizations, name='manage_organizations'),
]
