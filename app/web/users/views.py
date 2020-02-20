from django.contrib.auth import logout as logout
from django.http.response import HttpResponseRedirect


def generic_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
