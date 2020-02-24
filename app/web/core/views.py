from django.views.generic import TemplateView
from web.documents.models import *
from web.users.auth import auth_test


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        document_list = Document.objects.all()

        kwargs.update({
            'document_list': document_list
        })
        return super().get_context_data(**kwargs)
