from django.conf import settings
from django.urls import path, include as path_include
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from web.core.views import *
from web.health.views import health_default, health_db
from web.users.views import generic_logout, generic_login


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/settings', VariablesView.as_view(), name='variables'),
    path('admin/dumpdata', dumpdata, name='dumpdata'),
    path('admin/objectstore', ObjectStoreView.as_view(), name='objectstore'),
    path('admin/sendmail', SendMailView.as_view(), name='sendmail'),

    path('health', health_default),
    path('omslagroute/health', health_default),
    path('omslagroute/health-db', health_db),

    path('document/', path_include('web.documents.urls')),
    path('timeline/', path_include('web.timeline.urls')),
    path('organisaties/', path_include('web.organizations.urls')),
    path('gebruikers/', path_include('web.users.urls')),
    # path('formulieren/', include('web.forms.urls')),
    path('clienten/', path_include('web.cases.urls')),

    path('inloggen/', generic_login, name='inloggen'),
    path('uitloggen/', generic_logout, name='uitloggen'),

    url(r'^oidc/', include('keycloak_oidc.urls')),

    path('admin/', admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
