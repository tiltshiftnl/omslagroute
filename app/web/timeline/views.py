from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View
from .models import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import *
from web.users.auth import auth_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from web.users.auth import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required


@user_passes_test(auth_test, group_name='wonen')
def manage_timeline(request):
    Moment_FormSet = modelformset_factory(Moment, form=MomentForm, extra=1, can_delete=True)
    if request.method == 'POST':
        formset = Moment_FormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            for object in formset.deleted_objects:
                object.delete()
            return HttpResponseRedirect(reverse('manage_timeline'))

    else:
        formset = Moment_FormSet()
    return render(request, 'timeline/manage_moments.html', {
        'moment_form_set': formset
    })
