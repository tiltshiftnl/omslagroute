from django.contrib import admin
from .models import *


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Federation)
class FederationAdmin(admin.ModelAdmin):
    list_display = ('name', 'federation_id', 'main_email', 'organization')
