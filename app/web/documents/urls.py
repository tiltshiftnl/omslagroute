from .views import DocumentList, DocumentCreate
from django.urls import path


urlpatterns = [
    path('lijst', DocumentList.as_view(), name='documenten'),
    path('nieuw', DocumentCreate.as_view(), name='nieuw_document'),
]
