from .views import DocumentList, DocumentCreate
from django.urls import path


urlpatterns = [
    path('nieuw/<int:document>', DocumentCreate.as_view(), name='add_document_version_to_document'),
]
