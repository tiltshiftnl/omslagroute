from django.views.generic import TemplateView
from web.documents.models import *
from web.users.auth import auth_test


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        document_list = Document.objects.all()
        #if not auth_test(self.request.user, 'wonen'):
           #document_list.filter(document_to_document_version__isnull=False)

        kwargs.update({
            'document_list': document_list
        })
        print('HomePageView')
        return super().get_context_data(**kwargs)

