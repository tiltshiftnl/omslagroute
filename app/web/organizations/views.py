from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import *
from web.users.auth import auth_test
from django.forms import modelformset_factory
from django.shortcuts import render
from web.users.auth import user_passes_test
from web.users.statics import BEHEERDER


@user_passes_test(auth_test, user_type=BEHEERDER)
def manage_organizations(request):
    organization_formset = modelformset_factory(Organization, form=OrganizationForm, extra=1, can_delete=True)
    if request.method == 'POST':
        formset = organization_formset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            instances = formset.save()
            for instance in instances:
                instance.save()
            for object in formset.deleted_objects:
                object.delete()
            return HttpResponseRedirect(reverse('manage_organizations'))

    else:
        formset = organization_formset()
    return render(request, 'organizations/manage_organizations.html', {
        'formset': formset,
    })
