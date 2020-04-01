from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView, FormView
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import *
from web.users.auth import auth_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from web.users.statics import BEGELEIDER
from web.profiles.models import Profile
from web.forms.statics import URGENTIE_AANVRAAG, FIELDS_DICT
from web.forms.views import GenericModelFormView, GenericModelCreateFormView
from web.forms.forms import BaseGenericForm, GenericForm
import json
import sendgrid
from sendgrid.helpers.mail import Mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string


def form_completed(instance, sections):
    section_fields = BaseGenericForm._get_fields(sections)
    required_fields = [f for f in section_fields if FIELDS_DICT.get(f) and FIELDS_DICT.get(f).required]
    filled_fields = [f for f in required_fields if hasattr(instance, f) and getattr(instance, f)]
    print(len(required_fields))
    print(len(filled_fields))


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

    def get_context_data(self, **kwargs):
        completed = form_completed(self.object, URGENTIE_AANVRAAG)
        return super().get_context_data(**kwargs)


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


class GenericFormView(GenericModelFormView):
    model = Case
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseGenericModeForm

    def get_success_url(self):
        return reverse('case', kwargs={'pk': self.object.id})

    def get_discard_url(self):
        return reverse('case', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'sections': self.kwargs.get('sections'),
        })
        return kwargs

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, "Het formulier is ontvangen")
        return response

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            self.kwargs
        )
        return kwargs


class GenericCaseCreateFormView(GenericModelCreateFormView):
    model = Case
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseGenericModeForm

    def get_success_url(self):
        return reverse('cases_by_profile')

    def get_discard_url(self):
        return reverse('cases_by_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'sections': self.kwargs.get('sections'),
        })
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        case = form.save(commit=True)
        self.request.user.profile.cases.add(case)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangemaakt." % case.client_name)
        return response

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            self.kwargs
        )
        return kwargs


class SendCaseView(UpdateView):
    model = Case
    template_name = 'cases/send.html'
    form_class = SendCaseForm

    def get_success_url(self):
        return reverse('case', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        kwargs.update(self.kwargs)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        body = render_to_string('cases/mail/case.txt', {'case': self.object.to_dict()})
        to_email = form.cleaned_data['to_email']
        current_site = get_current_site(self.request)
        sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
        email = Mail(
            from_email='noreply@%s' % current_site.domain,
            to_emails=to_email,
            subject='Omslagroute - %s' % self.kwargs.get('title'),
            plain_text_content=body
        )
        sg.send(email)
        messages.add_message(
            self.request, messages.INFO, "De cliëntgegevens van '%s', zijn gestuurd naar '%s'." % (
                self.object.client_name,
                to_email
            )
        )
        return super().form_valid(form)

    def form_invalid(self, form):

        return super().form_invalid(form)










