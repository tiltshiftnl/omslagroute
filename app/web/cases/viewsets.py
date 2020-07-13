from rest_framework import viewsets, mixins, generics
from .models import CaseStatus, Case
from .statics import CASE_STATUS_INGEDIEND, CASE_STATUS_DICT
from .serializers import CaseStatusSerializer, CaseDossierNrSerializer
from django.contrib.auth.mixins import UserPassesTestMixin
from web.users.statics import BEGELEIDER, WONEN, PB_FEDERATIE_BEHEERDER, WONINGCORPORATIE_MEDEWERKER
from web.forms.statics import FORM_TITLE_BY_SLUG
from web.users.auth import auth_test
from web.users.utils import get_zorginstelling_medewerkers_email_list
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy, reverse
from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import Mail


class CaseStatusUpdateViewSet(UserPassesTestMixin, viewsets.ModelViewSet):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer

    def test_func(self):
        return auth_test(self.request.user, [WONEN, WONINGCORPORATIE_MEDEWERKER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        filters = ['case', 'form', 'status']
        get_vars = self.request.GET
        queryset = CaseStatus.objects.filter(
            case__in=Case.objects.by_user(self.request.user).values_list('id', flat=True),
        )
        kwargs = dict(('%s__in' % f, get_vars.getlist(f)) for f in filters if get_vars.getlist(f))
        return queryset.filter(**kwargs).order_by('-created')

    def create(self, request, *args, **kwargs):
        data = {'profile': request.user.profile.id}
        data.update(request.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if serializer.instance.status != CASE_STATUS_INGEDIEND:
            serializer.instance.case.create_version(serializer.instance.form)
            current_site = get_current_site(request)
            body = render_to_string('cases/mail/case_status_to_pb.txt', {
                'case_status': serializer.instance,
                'form_name': FORM_TITLE_BY_SLUG.get(serializer.instance.form),
                'case_form_url': 'https://%s%s' % (
                    current_site.domain,
                    reverse('update_case', kwargs={
                        'pk': serializer.instance.case.id,
                        'slug': serializer.instance.form,
                    })
                ),
            })
            email_adresses = get_zorginstelling_medewerkers_email_list(serializer.instance.case)
            if settings.SENDGRID_KEY and email_adresses:
                sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
                email = Mail(
                    from_email='noreply@%s' % current_site.domain,
                    to_emails=email_adresses,
                    subject='Omslagroute - %s, status: %s' % (
                        FORM_TITLE_BY_SLUG.get(serializer.instance.form),
                        CASE_STATUS_DICT.get(serializer.instance.status).get('current'),
                    ),
                    plain_text_content=body
                )
                sg.send(email)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CaseUpdateDossierNrViewSet(UserPassesTestMixin, viewsets.ViewSetMixin, generics.RetrieveUpdateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseDossierNrSerializer

    def test_func(self):
        return auth_test(self.request.user, [WONEN]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return Case._default_manager.by_user(user=self.request.user)