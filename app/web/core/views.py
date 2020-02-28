from django.views.generic import TemplateView
from web.documents.models import *
import os
from django.contrib.auth.mixins import UserPassesTestMixin


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        document_list = Document.objects.all()

        kwargs.update({
            'document_list': document_list
        })
        return super().get_context_data(**kwargs)


class VariablesView(UserPassesTestMixin, TemplateView):
    template_name = "variables.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        l = [[k, v] for k, v in os.environ.items()]
        l = sorted(l)

        kwargs.update({
            'var_list': dict(l),
        })
        return super().get_context_data(**kwargs)
