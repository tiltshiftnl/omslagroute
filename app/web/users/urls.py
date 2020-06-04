from .views import *
from django.urls import path


urlpatterns = [
    path('',  UserList.as_view(), name='user_list'),
    path('federatie/',  FederationUserList.as_view(), name='federation_user_list'),
    path('<int:pk>', UserUpdateView.as_view(), name="update_user"),
    path('federatie/<int:pk>/', FederationUserUpdateView.as_view(), name="update_federation_user"),
]
