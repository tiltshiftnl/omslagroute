from django.contrib.auth import logout, login
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import (
    AuthenticationForm, authenticate
)
from django.contrib import messages


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
