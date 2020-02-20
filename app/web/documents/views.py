from django.views.generic import *
from .models import Document
from django.urls import reverse_lazy


class DocumentList(ListView):
    model = Document
    template_name_suffix = 'en'


class DocumentCreate(CreateView):
    model = Document
    fields = ['title', 'uploaded_file', 'document_type']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('documenten')

