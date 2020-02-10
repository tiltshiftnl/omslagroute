from django.views.generic import TemplateView
import sys


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        print('Testing')
        return super().get_context_data(**kwargs)


