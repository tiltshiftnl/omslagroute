from django.contrib import admin
from .models import *


@admin.register(Organization)
class MomentAdmin(admin.ModelAdmin):
    list_display = ('name',)
