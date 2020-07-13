from django.views.generic import TemplateView, FormView, UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
import json
from json import JSONEncoder
import datetime
from .statics import FORMS_BY_SLUG
from django.http import Http404
from web.organizations.models import Federation


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class FormListView(TemplateView):
    template_name = 'forms/form_list_page.html'


class GenericFormView(FormView):
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('form_list')
    form_class = GenericForm

    def get_discard_url(self):
        return reverse_lazy('form_list')

    def get_initial(self):
        self.initial.update(json.loads(self.request.session.get('client_data', '{}')))
        return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'sections': self.kwargs.get('sections'),
        })
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['client_data'] = json.dumps(form.cleaned_data, cls=DateTimeEncoder)
        messages.add_message(self.request, messages.INFO, "Het formulier is ontvangen")
        return response

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            self.kwargs
        )
        kwargs.update({
            'discard_url': self.get_discard_url(),
        })
        return kwargs


class GenericUpdateFormView(UpdateView):
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('form_list')
    form_class = GenericModelForm

    def get_discard_url(self):
        return reverse_lazy('form_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        form_context = FORMS_BY_SLUG.get(self.kwargs.get('slug'))
        if not form_context:
            raise Http404
        kwargs.update({
            'form_context': form_context,
            'path': self.request.path,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        form_context = FORMS_BY_SLUG.get(self.kwargs.get('slug'), {})
        kwargs.update(
            self.kwargs
        )
        kwargs.update(form_context)
        kwargs.update({
            'discard_url': self.get_discard_url(),
            'federation': Federation.objects.filter(
                organization__federation_type=form_context.get('federation_type'),
            ).first(),
        })
        return kwargs


class GenericCreateFormView(CreateView):
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('form_list')
    form_class = GenericModelForm

    def get_discard_url(self):
        return reverse_lazy('form_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        form_context = FORMS_BY_SLUG.get(self.kwargs.get('slug'))
        if not form_context:
            raise Http404
        kwargs.update({
            'form_context': form_context,
            'path': self.request.path,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        form_context = FORMS_BY_SLUG.get(self.kwargs.get('slug'), {})
        kwargs.update(
            self.kwargs
        )
        kwargs.update(form_context)
        self.kwargs.update(form_context)
        kwargs.update({
            'discard_url': self.get_discard_url(),
            'title': form_context.get('title_new'),
        })
        return kwargs
