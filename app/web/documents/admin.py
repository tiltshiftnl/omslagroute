from django.contrib import admin
from .models import *


@admin.register(DocumentVersion)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('uploaded', 'document',)


@admin.register(Document)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
