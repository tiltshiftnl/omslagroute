from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .models import DocumentVersion, Document
from django.urls import reverse_lazy
from .forms import DocumentForm
from web.users.auth import auth_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


class DocumentList(UserPassesTestMixin, ListView):
    model = Document
    template_name_suffix = '_list'

    def test_func(self):
        return auth_test(self.request.user, 'wonen')


class DocumentDelete(UserPassesTestMixin, DeleteView):
    model = Document
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('document_list')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def delete(self, request, *args, **kwargs):
        response = super().delete(self, request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, "Het document '%s' is verwijderd." % self.object.name)
        return response


class DocumentCreate(UserPassesTestMixin, CreateView):
    model = Document
    fields = ('name', 'icon')
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('document_list')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, "Het document '%s' is aangemaakt." % self.object.name)
        return response


class DocumentUpdate(UserPassesTestMixin, UpdateView):
    model = Document
    fields = ('name', 'icon')
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('document_list')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, "Het document '%s' is aangepast." % self.object.name)
        return super().form_valid(form)


class DocumentVersionCreate(UserPassesTestMixin, CreateView):
    model = DocumentVersion
    form_class = DocumentForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'document': Document.objects.get(id=self.kwargs.get('document'))
        })
        return super().get_context_data(**kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['document'] = self.kwargs.get('document')
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, "De versie '%s' is aangemaakt." % self.object.uploaded_str)
        return response


class DocumentVersionDelete(UserPassesTestMixin, DeleteView):
    model = DocumentVersion
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('document_list')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')




