from django.views.generic import TemplateView, RedirectView
import os
import sys
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.storage import default_storage
from web.timeline.models import *
from web.documents.models import *
from web.organizations.models import *
from django.urls import reverse_lazy
import sendgrid
from sendgrid.helpers.mail import *
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .utils import *
from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from django.http import HttpResponse
from web.users.statics import BEHEERDER
from web.organizations.statics import FEDERATION_TYPE_ADW, FEDERATION_TYPE_ZORGINSTELLING
from web.users.auth import auth_test
from web.cases.statics import *
from web.cases.models import Case, CaseStatus
import datetime
import calendar


class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        document_list = Document.objects.all()
        floating_document_list = Document.objects.filter(moment__documents__isnull=True)
        moment_list = Moment.objects.all()
        organization_list = Organization.objects.all()

        kwargs.update({
            'document_list': document_list,
            'floating_document_list': floating_document_list,
            'moment_list': moment_list,
            'organization_list': organization_list,
        })
        return super().get_context_data(**kwargs)


class VariablesView(UserPassesTestMixin, TemplateView):
    template_name = "variables.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        l = [[k, v] for k, v in os.environ.items()]
        l = sorted(l)

        kwargs.update({
            'var_list': dict(l),
        })
        return super().get_context_data(**kwargs)


class ObjectStoreView(UserPassesTestMixin, TemplateView):
    template_name = "objectstore.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):

        documentversion_list = [{
            'name': d.uploaded_file.name,
            'generate_filename': default_storage.generate_filename(d.uploaded_file.name),
            'url': default_storage.url(default_storage.generate_filename(d.uploaded_file.name)),
            'exists': default_storage.exists(default_storage.generate_filename(d.uploaded_file.name)),
            'id': d.id
        } for d in DocumentVersion.objects.all()]

        kwargs.update({
            'objectstore_container_list': ['uploads/%s' % default_storage.get_valid_name(o) for o in default_storage.listdir('uploads')[1]],
            'documentversion_list': documentversion_list,
        })
        return super().get_context_data(**kwargs)


class SendMailView(UserPassesTestMixin, RedirectView):
    url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        mailadres = request.GET.get('mailadres')
        if mailadres:
            current_site = get_current_site(self.request)
            sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            email = Mail(
                from_email='noreply@%s' % current_site.domain,
                to_emails=mailadres,
                subject='Omslagroute - mail',
                plain_text_content='Het werkt!'
            )

            sg.send(email)

        return super().get(request, *args, **kwargs)


class DataView(UserPassesTestMixin, TemplateView):
    template_name = "data.html"

    def test_func(self):
        return auth_test(self.request.user, [BEHEERDER])

    def get_context_data(self, **kwargs):
        month = datetime.datetime.now().strftime('%m')
        year = datetime.datetime.now().strftime('%Y')
        monthrange = calendar.monthrange(int(year), int(month))
        try:
            monthrange = calendar.monthrange(int(self.request.GET.get('jaar')), int(self.request.GET.get('maand')))
            month = self.request.GET.get('maand')
            year = self.request.GET.get('jaar')
            
        except:
            print('querystring params wrong format')
        start_month = datetime.datetime(year=int(year), month=int(month), day=1)
        end_month = datetime.datetime(year=int(year), month=int(month), day=monthrange[1]) + datetime.timedelta(days=1)
        data = []
        zorginstelling_list = Federation.objects.filter(
            organization__federation_type=FEDERATION_TYPE_ZORGINSTELLING,
        )
        all_cases = Case.objects.all()
        next_month = end_month.strftime('?jaar=%Y&maand=%m') if end_month < datetime.datetime.now() else None 
        prev_month = (start_month - datetime.timedelta(days=1)).strftime('?jaar=%Y&maand=%m')

        for zorginstelling in zorginstelling_list:
            case_list = all_cases.filter(
                profile__user__federation=zorginstelling,
            )
            case_list_period = case_list.filter(
                created__gt=start_month,
                created__lte=end_month,
            )

            casestatus_list = CaseStatus.objects.filter(
                case__in=case_list,
            )
            urgentie = casestatus_list.filter(
                form=CASE_VERSION_FORM_URGENTIE,
            )
            omklap = casestatus_list.filter(
                form=CASE_VERSION_FORM_OMKLAP,
            )

            urgentie_ingediend = urgentie.filter(
                status=CASE_STATUS_INGEDIEND,
            )
            urgentie_ingediend_period = urgentie_ingediend.filter(
                created__gt=start_month,
                created__lte=end_month,
            )

            urgentie_goedgekeurd = urgentie.filter(
                status=CASE_STATUS_GOEDGEKEURD,
            )
            urgentie_goedgekeurd_period = urgentie_goedgekeurd.filter(
                created__gt=start_month,
                created__lte=end_month,
            )

            omklap_ingediend = omklap.filter(
                status=CASE_STATUS_INGEDIEND,
            )
            omklap_ingediend_period = omklap_ingediend.filter(
                created__gt=start_month,
                created__lte=end_month,
            )

            omklap_goedgekeurd = omklap.filter(
                status=CASE_STATUS_GOEDGEKEURD,
            )
            omklap_goedgekeurd_period = omklap_goedgekeurd.filter(
                created__gt=start_month,
                created__lte=end_month,
            )

            user_list = User.objects.filter(
                federation=zorginstelling,
            )
            data.append({
                'zorginstelling': zorginstelling,
                'case_list': case_list,
                'case_list_period': case_list_period,
                'user_list': user_list,
                'urgentie_ingediend': urgentie_ingediend.order_by('case__id', 'created').distinct('case__id'),
                'urgentie_ingediend_period': urgentie_ingediend_period.order_by('case__id', 'created').distinct('case__id'),
                'urgentie_goedgekeurd': urgentie_goedgekeurd.order_by('case__id', '-created').distinct('case__id'),
                'urgentie_goedgekeurd_period': urgentie_goedgekeurd_period.order_by('case__id', '-created').distinct('case__id'),
                'omklap_ingediend': omklap_ingediend.order_by('case__id', 'created').distinct('case__id'),
                'omklap_ingediend_period': omklap_ingediend_period.order_by('case__id', 'created').distinct('case__id'),
                'omklap_goedgekeurd': omklap_goedgekeurd.order_by('case__id', '-created').distinct('case__id'),
                'omklap_goedgekeurd_period': omklap_goedgekeurd_period.order_by('case__id', '-created').distinct('case__id'),
            })
        kwargs.update({
            'zorginstelling_list': data,
            'all_cases': all_cases,
            'start_month': start_month,
            'next_month': next_month,
            'prev_month': prev_month,
        })
        return super().get_context_data(**kwargs)



@user_passes_test(lambda u: u.is_superuser)
def dumpdata(request):
    sysout = sys.stdout
    fname = "%s-%s.json" % ('omslagroute', settings.SOURCE_COMMIT.strip())
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname

    sys.stdout = response
    call_command('dumpdata', 'organizations', 'documents', 'timeline', '--indent=4')
    sys.stdout = sysout

    return response
