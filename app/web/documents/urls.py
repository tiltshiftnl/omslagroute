from .views import DocumentList, DocumentCreate
from django.urls import path


urlpatterns = [
    path('lijst', DocumentList.as_view(), name='documenten'),
    path('nieuw/<int:document_type>', DocumentCreate.as_view(), name='add_document_to_type'),
]
