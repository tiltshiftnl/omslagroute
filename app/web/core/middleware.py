from web.users.forms import (
    AuthenticationForm
)
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, authenticate


class LoginFormMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        form = AuthenticationForm(request)
        if request.method == 'POST' and 'is_top_login_form' in request.POST:
            print('before AuthenticationForm')
            form = AuthenticationForm(data=request.POST)
            print('after AuthenticationForm')
            if form.is_valid():
                print('before login')
                login(request, form.get_user())
                print('after login')
                print(request.user.groups.all())
                # if request.user.is_authenticated:
                return HttpResponseRedirect(request.POST.get('next', '/'))
            else:
                print('not valid')

        # attach the form to the request so it can be accessed within the templates
        print(form)

        request.login_form = form
        response = self.get_response(request)
        print(response)

        return response


