from .views import *
from django.urls import path


urlpatterns = [
    path('', FeedbackFormView.as_view(), name='feedback'),
]
