from django.contrib.auth import logout, login
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import (
    AuthenticationForm, authenticate
)
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from web.users.auth import auth_test
from django.db import transaction


def generic_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Je bent uitgelogd')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def generic_login(request):
    if request.method == 'POST' and 'is_top_login_form' in request.POST:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            return HttpResponseRedirect(request.POST.get('next', '/'))
    messages.add_message(request, messages.ERROR, 'Er is iets mis gegaan met het inloggen')
    return HttpResponseRedirect('%s#login' % (request.POST.get('next', '/')))


class UserList(UserPassesTestMixin, ListView):
    model = User
    template_name_suffix = '_list_page'
    queryset = User.objects.filter(is_staff=False, is_superuser=False)

    def test_func(self):
        return self.request.user.is_superuser


class UserCreate(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['profileformset'] = ProfileFormSet(self.request.POST, self.request.FILES)
        else:
            data['profileformset'] = ProfileFormSet()
        return data

    def form_invalid(self, form):
        respond = super().form_invalid(form)
        for k, v in form.errors.items():
            for e in v:
                messages.add_message(self.request, messages.ERROR, e)
        return respond

    def form_valid(self, form):
        context = self.get_context_data()
        profileformset = context['profileformset']
        with transaction.atomic():
            self.object = form.save()
            if profileformset.is_valid():
                print(profileformset)
                print(type(profileformset.instance))
                print(type(self.object))
                profileformset.instance = self.object
                profileformset.save()
                profileformset.instance.save()

        messages.add_message(self.request, messages.INFO, "De gebruiker '%s' is aangemaakt" % self.object.username)
        return super().form_valid(form)
