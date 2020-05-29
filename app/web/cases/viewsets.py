from rest_framework import viewsets, mixins
from .models import CaseStatus
from .statics import CASE_STATUS_INGEDIEND
from .serializers import CaseStatusSerializer
from django.contrib.auth.mixins import UserPassesTestMixin
from web.users.statics import BEGELEIDER, WONEN
from web.forms.statics import FORM_TITLE_BY_SLUG
from web.users.auth import auth_test
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
        return auth_test(self.request.user, [BEGELEIDER, WONEN]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return CaseStatus.objects.all().order_by('-created')

    def create(self, request, *args, **kwargs):
        data = {'profile': request.user.profile.id}
        data.update(request.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if serializer.instance.status != CASE_STATUS_INGEDIEND:
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
            email_adresses = list(serializer.instance.case.profile_set.all().values_list('user__username', flat=True))
            if settings.SENDGRID_KEY:
                sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
                email = Mail(
                    from_email='noreply@%s' % current_site.domain,
                    to_emails=email_adresses,
                    subject='Omslagroute - %s' % FORM_TITLE_BY_SLUG.get(serializer.instance.form),
                    plain_text_content=body
                )
                sg.send(email)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)