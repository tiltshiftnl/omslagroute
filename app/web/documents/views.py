from django.views.generic import CreateView, DeleteView, ListView
from .models import DocumentVersion, Document
from django.urls import reverse_lazy
from .forms import DocumentForm


class DocumentList(ListView):
    model = Document
    template_name_suffix = '_list'


class DocumentDelete(DeleteView):
    model = Document
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('document_list')


class DocumentCreate(CreateView):
    model = Document
    fields = ('name', 'icon')
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('document_list')


class DocumentVersionCreate(CreateView):
    model = DocumentVersion
    form_class = DocumentForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['document'] = self.kwargs.get('document')
        return initial




