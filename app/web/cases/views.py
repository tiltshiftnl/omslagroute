from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView, FormView
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
from web.users.statics import BEGELEIDER
from web.profiles.models import Profile
from web.forms.forms import GenericModelForm
import json


class UserCaseList(UserPassesTestMixin, ListView):
    model = Case
    template_name_suffix = '_list_page'

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        # qs = super().get_queryset()
        # profile = get_object_or_404(Profile, id=self.request.user.profile.id)
        return self.request.user.profile.cases.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        # self.profile = self.request.user.profile
        return super().get_context_data(object_list=object_list, **kwargs)


class CaseDetailView(UserPassesTestMixin, DetailView):
    model = Case
    template_name_suffix = '_page'

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')


class CaseCreateView(UserPassesTestMixin, CreateView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('cases_by_profile')

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def form_valid(self, form):
        case = form.save(commit=True)
        self.request.user.profile.cases.add(case)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangemaakt." % case.client_name)
        return super().form_valid(form)


class CaseUpdateView(UserPassesTestMixin, UpdateView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('cases_by_profile')

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangepast." % self.object.client_name)
        return super().form_valid(form)


class CaseDeleteView(UserPassesTestMixin, DeleteView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('cases_by_profile')

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def delete(self, request, *args, **kwargs):
        response = super().delete(self, request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is verwijderd." % self.object.client_name)
        return response


class GenericFormView(UpdateView):
    model = Case
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseGenericModeForm

    def get_success_url(self):
        return reverse_lazy('cases_by_profile')

    # def get_initial(self):
    #     #self.initial.update(json.loads(self.request.session.get('client_data', '{}')))
    #     return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'sections': self.kwargs.get('sections'),
        })
        return kwargs

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        #self.request.session['client_data'] = json.dumps(form.cleaned_data, cls=DateTimeEncoder)
        messages.add_message(self.request, messages.INFO, "Het formulier is ontvangen")
        return response

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            self.kwargs
        )
        return kwargs

