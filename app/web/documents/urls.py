from .views import DocumentDelete, DocumentList, DocumentVersionCreate, DocumentCreate
from django.urls import path


urlpatterns = [
    path('', DocumentList.as_view(), name='document_list'),
    path('nieuw', DocumentCreate.as_view(), name='document_create'),
    path('delete/<int:pk>', DocumentDelete.as_view(), name='document_delete'),
    path('nieuw/<int:document>', DocumentVersionCreate.as_view(), name='add_document_version_to_document'),
]
