from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.http.response import HttpResponseRedirect


class LoginFormMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method == 'POST' and 'is_top_login_form' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                from django.contrib.auth import login
                login(request, form.get_user())

                return HttpResponseRedirect(request.POST.get('next', '/'))

        else:
            form = AuthenticationForm(request)

        # attach the form to the request so it can be accessed within the templates
        request.login_form = form

        response = self.get_response(request)

        return response


