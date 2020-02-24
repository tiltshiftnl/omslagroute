from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from web.core.views import HomePageView
from web.health.views import health_default, health_db
from web.users.views import generic_logout, generic_login


urlpatterns = [
    path('omslagroute/', include('web.urls')),

]
