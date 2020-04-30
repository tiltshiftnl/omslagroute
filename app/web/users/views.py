from django.contrib.auth import logout, login
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import (
    AuthenticationForm, authenticate
)
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, FormView
from .models import *
from .forms import *
from django.urls import reverse_lazy, reverse
from web.users.auth import auth_test
from django.db import transaction
from .statics import BEGELEIDER, BEHEERDER, USER_TYPES_ACTIVE
from mozilla_django_oidc.views import OIDCAuthenticationRequestView as DatapuntOIDCAuthenticationRequestView
from django.core.paginator import Paginator
import operator
from django.db.models import Avg, Count

try:
    from urllib.parse import urlencode
except ImportError:
    # Python < 3
    from urllib import urlencode

from mozilla_django_oidc.views import get_next_url, get_random_string


def generic_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Je bent uitgelogd')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def generic_login(request):
    if request.method == 'POST' and 'is_top_login_form' in request.POST:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                if user.user_type == BEGELEIDER:
                    return HttpResponseRedirect(reverse('cases_by_profile'))
                return HttpResponseRedirect(request.POST.get('next', '/'))
    messages.add_message(request, messages.ERROR, 'Er is iets mis gegaan met het inloggen')
    return HttpResponseRedirect('%s#login' % (request.POST.get('next', '/')))


class UserList(UserPassesTestMixin, FormView):
    # model = User
    template_name_suffix = '_list_page'
    template_name = 'users/user_list_page.html'
    # queryset = User.objects.all()
    form_class = FilterListForm

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        filter = self.request.GET.getlist('filter', USER_TYPES_ACTIVE)
        object_list = User.objects.all().filter(user_type__in=filter)

        # default sort on user_type by custom list
        object_list = [[o, USER_TYPES_ACTIVE.index(o.user_type)] for o in object_list]
        object_list = sorted(object_list, key=lambda o: o[1])
        object_list = [o[0] for o in object_list]

        paginator = Paginator(object_list, 20)
        page = self.request.GET.get('page', 1)
        object_list = paginator.get_page(page)
        filter_form = FilterListForm()
        kwargs.update({
            'object_list': object_list,
            # 'filter_form': filter_form,
        })
        return kwargs
    #
    # def get(self, request, *args, **kwargs):
    #     filter_form = FilterListForm(request)
    #     kwargs.update({
    #         'filter_form': filter_form,
    #     })
    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     kwargs = super().get_context_data(object_list=object_list, **kwargs)
    #     filter = self.request.GET.getlist('filter', USER_TYPES_ACTIVE)
    #     object_list = User.objects.all().filter(user_type__in=filter)
    #
    #     # default sort on user_type by custom list
    #     object_list = [[o, USER_TYPES_ACTIVE.index(o.user_type)] for o in object_list]
    #     object_list = sorted(object_list, key=lambda o: o[1])
    #     object_list = [o[0] for o in object_list]
    #
    #     paginator = Paginator(object_list, 20)
    #     page = self.request.GET.get('page', 1)
    #     object_list = paginator.get_page(page)
    #     filter_form = FilterListForm()
    #     kwargs.update({
    #         'object_list': object_list,
    #         # 'filter_form': filter_form,
    #     })
    #     return kwargs

    def test_func(self):
        return auth_test(self.request.user, BEHEERDER)


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    template_name_suffix = '_update_form'
    form_class = UserCreationForm
    success_url = reverse_lazy('user_list')

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
        messages.add_message(self.request, messages.INFO, "Gebruiker %s is aangemaakt" % user.username)
        return super().form_valid(form)


class OIDCAuthenticationRequestView(DatapuntOIDCAuthenticationRequestView):
    def get(self, request):
        """OIDC client authentication initialization HTTP endpoint"""
        state = get_random_string(self.get_settings('OIDC_STATE_SIZE', 32))
        redirect_field_name = self.get_settings('OIDC_REDIRECT_FIELD_NAME', 'next')
        reverse_url = self.get_settings('OIDC_AUTHENTICATION_CALLBACK_URL',
                                        'oidc_authentication_callback')

        params = {
            'response_type': 'code',
            'scope': self.get_settings('OIDC_RP_SCOPES', 'openid email'),
            'client_id': self.OIDC_RP_CLIENT_ID,
            'redirect_uri': 'https://acc.omslagroute.amsterdam.nl%s' % reverse(reverse_url),
            'state': state,
        }

        params.update(self.get_extra_params(request))

        if self.get_settings('OIDC_USE_NONCE', True):
            nonce = get_random_string(self.get_settings('OIDC_NONCE_SIZE', 32))
            params.update({
                'nonce': nonce
            })
            request.session['oidc_nonce'] = nonce

        request.session['oidc_state'] = state
        request.session['oidc_login_next'] = get_next_url(request, redirect_field_name)

        query = urlencode(params)
        print(query)
        redirect_url = '{url}?{query}'.format(url=self.OIDC_OP_AUTH_ENDPOINT, query=query)
        return HttpResponseRedirect(redirect_url)
