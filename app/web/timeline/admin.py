from django.contrib import admin
from .models import *


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ('name', 'order',)
