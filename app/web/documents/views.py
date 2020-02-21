from django.views.generic import *
from .models import Document
from django.urls import reverse_lazy
from .forms import DocumentForm


class DocumentList(ListView):
    model = Document
    template_name_suffix = 'en'


class DocumentCreate(CreateView):
    model = Document
    form_class = DocumentForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['document_type'] = self.kwargs.get('document_type')
        return initial



