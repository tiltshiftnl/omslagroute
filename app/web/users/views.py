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
from django.urls import reverse_lazy, reverse
from web.users.auth import auth_test
from django.db import transaction
from .statics import BEGELEIDER, BEHEERDER


def generic_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Je bent uitgelogd')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def generic_login(request):
    if request.method == 'POST' and 'is_top_login_form' in request.POST:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.user_type == BEGELEIDER:
                return HttpResponseRedirect(reverse('cases_by_profile'))
            return HttpResponseRedirect(request.POST.get('next', '/'))
    messages.add_message(request, messages.ERROR, 'Er is iets mis gegaan met het inloggen')
    return HttpResponseRedirect('%s#login' % (request.POST.get('next', '/')))


class UserList(UserPassesTestMixin, ListView):
    model = User
    template_name_suffix = '_list_page'
    queryset = User.objects.filter(is_staff=False, is_superuser=False)

    def test_func(self):
        return auth_test(self.request.user, BEHEERDER)


class UserCreationView(UserPassesTestMixin, CreateView):
    model = User
    template_name_suffix = '_create_form'
    form_class = UserCreationForm
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return auth_test(self.request.user, BEHEERDER)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['profile_form'] = ProfileForm(self.request.POST, self.request.FILES)
        else:
            data['profile_form'] = ProfileForm()
        return data

    def post(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()
        profile_form = context['profile_form']
        form = self.get_form()

        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))

    def form_valid(self, form, profile_form):
        user = form.save(commit=True)
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.add_message(self.request, messages.INFO, "De gebruiker '%s' is aangemaakt" % user.username)
        return super().form_valid(form)
