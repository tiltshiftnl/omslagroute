from django.views.generic import *
from .models import DocumentVersion
from django.urls import reverse_lazy
from .forms import DocumentForm


class DocumentList(ListView):
    model = DocumentVersion
    template_name_suffix = 'en'


class DocumentCreate(CreateView):
    model = DocumentVersion
    form_class = DocumentForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['document'] = self.kwargs.get('document')
        return initial



