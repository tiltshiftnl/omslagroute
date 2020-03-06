from .views import *
from django.urls import path


urlpatterns = [
    path('',  manage_timeline, name='manage_timeline'),
    path('update-moment/<int:pk>', MomentUpdateView.as_view(), name="update_moment"),
    path('create-moment', create_moment, name="create_moment"),
    path('order', order_timeline, name="order_timeline"),
]
