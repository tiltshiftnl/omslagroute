from .views import *
from django.urls import path


urlpatterns = [
    path('',  UserList.as_view(), name='user_list'),
    path('nieuw', UserCreationView.as_view(), name="add_user"),
]
