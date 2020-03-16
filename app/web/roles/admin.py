from django.contrib import admin
from .models import *


@admin.register(Role)
class MomentAdmin(admin.ModelAdmin):
    list_display = ('name',)
