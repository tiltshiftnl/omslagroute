from .views import *
from django.urls import path


urlpatterns = [
    path('',  manage_timeline, name='manage_timeline'),
    path('update-moment', update_moment, name="update_moment"),
    path('delete-moment', delete_moment, name="delete_moment"),
    path('order', order_timeline, name="order_timeline"),
]
