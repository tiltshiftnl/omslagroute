from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .models import *
from django.urls import reverse_lazy
from .forms import *
from web.users.auth import auth_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http.response import HttpResponse, HttpResponseForbidden, FileResponse, Http404, HttpResponseRedirect
from django.forms.models import inlineformset_factory
from web.timeline.models import Moment
from django.core.files.storage import default_storage
from django.utils.html import mark_safe
from django.conf import settings
import urllib
import requests
from urllib.request import urlopen


class DocumentList(UserPassesTestMixin, ListView):
    model = Document
    template_name_suffix = '_list_page'

    def test_func(self):
        return auth_test(self.request.user, 'wonen')


class DocumentDelete(UserPassesTestMixin, DeleteView):
    model = Document
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def delete(self, request, *args, **kwargs):
        response = super().delete(self, request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, "Het document '%s' is verwijderd." % self.object.name)
        return response


class DocumentCreate(UserPassesTestMixin, CreateView):
    model = Document
    fields = ('name', 'document_type')
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, "Het document '%s' is aangemaakt." % self.object.name)
        return response


class DocumentUpdate(UserPassesTestMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def form_valid(self, form):
        response = super().form_valid(form)
        for moment in self.object.moment_set.all():
            moment.documents.remove(self.object)
        if form.cleaned_data.get("moment_list"):
            form.cleaned_data.get("moment_list").documents.add(self.object)
        messages.add_message(self.request, messages.INFO, "Het document '%s' is aangepast." % self.object.name)

        return response

    def form_invalid(self, form):
        for k, v in form.errors.items():
            for e in v:
                messages.add_message(self.request, messages.ERROR, e)
        return super().form_invalid(form)


class DocumentVersionCreate(UserPassesTestMixin, CreateView):
    model = DocumentVersion
    form_class = DocumentVersionForm
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
    success_url = reverse_lazy('home')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')


class DocumentVersionFormSetCreate(UserPassesTestMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name_suffix = '_and_docversion_create_form'
    success_url = reverse_lazy('home')

    def test_func(self):
        return auth_test(self.request.user, 'wonen')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['documentversionformset'] = DocumentVersionFormSet(self.request.POST, self.request.FILES)
        else:
            data['documentversionformset'] = DocumentVersionFormSet()
        return data

    def form_invalid(self, form):
        respond = super().form_invalid(form)
        for k, v in form.errors.items():
            for e in v:
                messages.add_message(self.request, messages.ERROR, e)
        return respond

    def form_valid(self, form):
        context = self.get_context_data()
        documentversionformset = context['documentversionformset']
        with transaction.atomic():
            self.object = form.save()
            if documentversionformset.is_valid():
                documentversionformset.instance = self.object
                documentversionformset.save()

        messages.add_message(self.request, messages.INFO, "Het document '%s' is aangemaakt" % self.object.name)
        return super().form_valid(form)


class CreateDocumentAddToMoment(DocumentVersionFormSetCreate):
    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        get_object_or_404(Moment, pk=self.kwargs.get('moment_id'))
        initial['moment_id'] = self.kwargs.get('moment_id')
        return initial

    def form_valid(self, form):
        valid = super().form_valid(form)
        moment_id = self.kwargs.get('moment_id')
        moment = Moment.objects.get(id=moment_id) if Moment.objects.filter(id=moment_id).count() else None
        if moment:
            with transaction.atomic():
                moment.documents.add(self.object)
        messages.add_message(self.request, messages.INFO, "Het aangemaakte document is toegevoegd aan de processtap '%s'" % moment.name)
        return valid


def download_documentversion(request, id):
    documentversion = get_object_or_404(DocumentVersion, id=id)
    if not default_storage.exists(default_storage.generate_filename(documentversion.uploaded_file.name)):
        raise Http404()

    return HttpResponseRedirect(documentversion.uploaded_file.url)
