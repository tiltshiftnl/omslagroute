from django.views.generic import TemplateView
from web.documents.models import *
import os
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.storage import default_storage
from django.conf import settings
import logging
from swift.storage import SwiftStorage

from swiftclient.service import SwiftService, SwiftError
from sys import argv


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


class ObjectStoreView(UserPassesTestMixin, TemplateView):
    template_name = "objectstore.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):

        object_list = default_storage.listdir('uploads')[1]
        for o in object_list:
            print(default_storage.url(o))
            print(default_storage.exists('uploads/%s' % default_storage.get_valid_name(o)))

        kwargs.update({
            'objectstore_container_list': ['uploads/%s' % default_storage.get_valid_name(o) for o in default_storage.listdir('uploads')[1]],
            'document_list': Document.objects.all(),
        })
        return super().get_context_data(**kwargs)
