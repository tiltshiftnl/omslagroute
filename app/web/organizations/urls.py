from .views import *
from django.urls import path


urlpatterns = [
    path('', FederationListView.as_view(), name='federation_list'),
    path('nieuwe-organisatie/', FederationCreateView.as_view(), name='federation_create'),
    path('organisatie/<int:pk>/', FederationUpdateView.as_view(), name='federation_update'),
    path('verwijder-organisatie/<int:pk>/', FederationDeleteView.as_view(), name='federation_delete'),
]
