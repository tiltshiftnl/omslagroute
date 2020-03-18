from django.contrib import admin
from .models import *


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client_first_name',
        'client_last_name',
    )
