from django.contrib.auth import logout, login
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import (
    AuthenticationForm, authenticate
)


def generic_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def generic_login(request):
    if request.method == 'POST' and 'is_top_login_form' in request.POST:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            return HttpResponseRedirect(request.POST.get('next', '/'))

    return HttpResponseRedirect('%s?error=login' % (request.POST.get('next', '/')))
