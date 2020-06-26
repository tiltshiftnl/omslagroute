from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView, FormView, TemplateView
from .models import *
from .statics import CASE_STATUS_AFGEKEURD, CASE_STATUS_GOEDGEKEURD, CASE_STATUS_IN_BEHANDELING, CASE_STATUS_INGEDIEND
from django.urls import reverse_lazy, reverse
from .forms import *
from web.users.auth import auth_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from web.users.statics import BEGELEIDER, WONEN, PB_FEDERATIE_BEHEERDER
from web.profiles.models import Profile
from web.forms.statics import URGENTIE_AANVRAAG, FORMS_BY_SLUG, BASIS_GEGEVENS, FORM_TITLE_BY_SLUG
from web.forms.views import GenericUpdateFormView, GenericCreateFormView
from web.forms.utils import get_sections_fields
import sendgrid
from sendgrid.helpers.mail import Mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from web.organizations.models import Organization
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from web.users.auth import user_passes_test
from django.core.paginator import Paginator
from web.timeline.models import Moment
from formtools.wizard.views import SessionWizardView
from django.db.models import Count
from django.db.models.functions import Concat
from django.db.models import TextField, DateTimeField, IntegerField
from django.core.exceptions import PermissionDenied
import datetime


class UserCaseList(UserPassesTestMixin, ListView):
    model = Case
    template_name_suffix = '_list_page'

    def test_func(self):
        return auth_test(self.request.user, [PB_FEDERATIE_BEHEERDER, BEGELEIDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all().order_by('-saved')

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs = super().get_context_data(object_list=object_list, **kwargs)
        # pagination
        object_list = kwargs.pop('object_list')
        paginator = Paginator(object_list, 20)
        page = self.request.GET.get('page', 1)
        object_list = paginator.get_page(page)
        kwargs.update({
            'object_list': object_list,
        })
        return kwargs


class UserCaseListAll(UserPassesTestMixin, TemplateView):
    template_name = 'cases/case_list_page_wonen.html'

    def test_func(self):
        return auth_test(self.request.user, WONEN) and hasattr(self.request.user, 'profile')

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        qs = CaseStatus.objects.all().exclude(status=CASE_STATUS_INGEDIEND)
        qs = qs.order_by('-created')
        qs = qs.annotate(distinct_name=Concat('case', 'form', output_field=TextField()))
        qs = qs.order_by('distinct_name', '-created')
        qs = qs.distinct('distinct_name')
        all_objects = CaseStatus.objects.all().order_by('-created')
        tabs_ids = [s.id for s in qs]
        final_set = all_objects.filter(id__in=tabs_ids)


        ingediend = CaseStatus.objects.all()
        ingediend = ingediend.order_by('-created')
        ingediend = ingediend.annotate(distinct_name=Concat('case', 'form', output_field=TextField()))
        ingediend = ingediend.order_by('distinct_name', '-created')
        ingediend = ingediend.distinct('distinct_name')
        ingediend_final_set = CaseStatus.objects.all().order_by('-created')
        ingediend_final_set = ingediend_final_set.filter(id__in=[s.id for s in ingediend])
        ingediend_final_set = ingediend_final_set.filter(status=CASE_STATUS_INGEDIEND)

        tabs = [
            [CASE_STATUS_INGEDIEND, 'Ingediend'],
            [CASE_STATUS_IN_BEHANDELING, 'In behandeling'],
            [CASE_STATUS_GOEDGEKEURD, 'Goedgekeurd'],
            [CASE_STATUS_AFGEKEURD, 'Afgekeurd'],
            [0, 'Alle'],
        ]
        tabs = [{
            'filter':t[0],  
            'title':t[1],  
            'queryset':final_set.filter(status=t[0]) if t[0] else final_set,  
        } for t in tabs]

        tabs[0]['queryset'] = ingediend_final_set

        tab_all_ids = [s.id for s in ingediend_final_set if s.is_first_of_statustype] + tabs_ids

        tabs[4]['queryset'] = all_objects.filter(id__in=set(tab_all_ids))

        paginator = Paginator(tabs[int(self.request.GET.get('f', 0))].get('queryset'), 20)
        page = self.request.GET.get('page', 1)
        object_list = paginator.get_page(page)

        kwargs.update({
            'object_list': paginator.get_page(page),
            'tabs': tabs,
        })
        return kwargs


class CaseDocumentList(UserPassesTestMixin, DetailView):
    model = Case
    template_name_suffix = '_document_list_page'

    def test_func(self):
        return auth_test(self.request.user, [PB_FEDERATIE_BEHEERDER, BEGELEIDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'document_list': Document.objects.filter(case=self.object)
        })
        return super().get_context_data(**kwargs)


class CaseDetailView(UserPassesTestMixin, DetailView):
    model = Case
    template_name_suffix = '_page'

    def get_context_data(self, **kwargs):
        linked_users = User.objects.filter(
            profile__in=self.object.profile_set.filter(
                user__user_type__in=[PB_FEDERATIE_BEHEERDER, BEGELEIDER]
            ).exclude(
                user=self.request.user
            )
        )
        # self.object.delete_related()
        kwargs.update({
            'moment_list': Moment.objects.all(),
            'basis_gegevens_fields': get_sections_fields(BASIS_GEGEVENS),
            'linked_users':  linked_users,
        })
        return super().get_context_data(**kwargs)

    def test_func(self):
        return auth_test(self.request.user, [WONEN, BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        if self.request.user.user_type in [BEGELEIDER, PB_FEDERATIE_BEHEERDER]:
            return self.request.user.profile.cases.all()
        case_list = CaseVersion.objects.order_by('case').distinct().values_list('case')
        return super().get_queryset().filter(id__in=case_list)


class CaseVersionFormDetailView(UserPassesTestMixin, DetailView):
    model = Case
    template_name_suffix = '_form_status'

    def get_context_data(self, **kwargs):
        form_data = FORMS_BY_SLUG.get(self.kwargs.get('slug'))
        kwargs.update({
            'form_fields': get_sections_fields(form_data.get('sections')),
            'form_data': FORMS_BY_SLUG.get(self.kwargs.get('slug')),
            'user_list': ', '.join(list([u for u in self.object.profile_set.all().values_list('user__username', flat=True) if u])),
            'document_list': self.object.document_set.filter(forms__contains=self.kwargs.get('slug')),
        })
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        case_list = CaseVersion.objects.order_by('case').distinct().values_list('case')
        if self.request.user.user_type in [BEGELEIDER, PB_FEDERATIE_BEHEERDER]:
            return Case.objects.filter(id__in=self.request.user.profile.cases.all().values_list('id', flat=True))
        return super().get_queryset().filter(id__in=case_list)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def test_func(self):
        return auth_test(self.request.user, [WONEN]) and hasattr(self.request.user, 'profile')


class CaseDetailAllDataView(CaseDetailView):
    template_name_suffix = '_page_all_data'


class CaseCreateView(UserPassesTestMixin, CreateView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('cases_by_profile')

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def form_valid(self, form):
        case = form.save(commit=True)
        self.request.user.profile.cases.add(case)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangemaakt." % case.client_name)
        return super().form_valid(form)


class CaseUpdateView(UserPassesTestMixin, UpdateView):
    model = Case
    form_class = CaseForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('cases_by_profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangepast." % self.object.client_name)
        return super().form_valid(form)


class CaseDeleteView(UserPassesTestMixin, DeleteView):
    model = Case
    template_name_suffix = '_delete'
    success_url = reverse_lazy('case_list')

    def test_func(self):
        return auth_test(self.request.user, [WONEN]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        case_list = CaseVersion.objects.order_by('case').distinct().values_list('case')
        return super().get_queryset().filter(id__in=case_list)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is verwijderd." % obj.client_name)
        return response


class CaseDeleteRequestView(UserPassesTestMixin, UpdateView):
    model = Case
    template_name_suffix = '_delete_request'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseDeleteRequestForm

    def get_success_url(self):
        return './?iframe=%s' % (
            self.success_url,
        )

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def form_valid(self, form):
        case = form.save(commit=False)
        case.delete_request_date = datetime.datetime.now()
        case.save()

        recipient_list = list(o[0] for o in Organization.objects.filter(main_email__isnull=False).values_list('main_email'))
        if form.cleaned_data.get('extra_recipient'):
            recipient_list.append(form.cleaned_data.get('extra_recipient'))
        recipient_list = set(recipient_list)
        current_site = get_current_site(self.request)
        body = render_to_string('cases/mail/case_delete_request.txt', {
            'case': case,
            'case_url': 'https://%s%s' % (
                current_site.domain,
                reverse('case', kwargs={
                    'pk': case.id,
                })
            ),
            'user': self.request.user,
        })
        if settings.SENDGRID_KEY:
            sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            email = Mail(
                from_email='noreply@%s' % current_site.domain,
                to_emails=recipient_list,
                subject='Omslagroute - Verzoek verwijderen cliënt',
                plain_text_content=body
            )
            sg.send(email)

        messages.add_message(self.request, messages.INFO, "Het verwijder verzoek is verstuurd.")
        return super().form_valid(form)


class GenericCaseUpdateFormView(UserPassesTestMixin, GenericUpdateFormView):
    model = Case
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseGenericModelForm

    def get_initial(self):
        self.initial.update({
            'document_list': Document.objects.filter(case=self.object, forms__contains=self.kwargs.get('slug'))
        })
        return super().get_initial()

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def get_success_url(self):
        next = self.request.POST.get('next')
        default_url = reverse('update_case', kwargs={'pk': self.object.id, 'slug': self.kwargs.get('slug')})
        percentage = self.object.status(FORMS_BY_SLUG.get(self.kwargs.get('slug'), {}).get('sections')).get('percentage')
        if percentage < 100 and next:
            return '%s?control=1' % default_url
        if next:
            return next
        return default_url

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        value_key = 'value'
        version_key = 'version_verbose'
        saved_key = 'saved'
        object_dict = self.object.to_dict()
        ld = [cv.to_dict() for cv in CaseVersion.objects.filter(case=self.object).order_by('-saved')]
        ld = ld if ld else [{}]
        dl = {k: [{
            value_key: dic[k].get('value'),
            version_key: FORMS_BY_SLUG.get(dic[version_key].get('value')).get('title'),
            saved_key: dic[saved_key].get('value'),
        } for dic in ld] for k in ld[0] if self.object.to_dict().get(k)}
        dl = {k: [
            vv for vv in v if vv.get(value_key) != '—' and vv.get(value_key) != object_dict.get(k, {}).get('value')
        ] for k, v in dl.items()}
        # remove double values
        dl = {k: [
            v[i] for i in range(len(v)) if i == 0 or v[i].get('value') != v[i-1].get('value')
        ] for k, v in dl.items()}
        kwargs.update({
            'case_versions': dl,
            'case_status_list': CaseStatus.objects.filter(case=self.object, form=self.kwargs.get('slug')).order_by('-created')
        })
        return kwargs

    def get_discard_url(self):
        return reverse('case', kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        slug = self.kwargs.get('slug')
        self.object.saved_by = self.request.user.profile
        self.object.saved_form = slug
        self.object.save()
        document_list = form.cleaned_data.get('document_list')
        for doc in form.fields['document_list'].queryset:
            if doc in document_list and slug not in doc.forms:
                doc.forms.append(slug)
            elif doc not in document_list and slug in doc.forms:
                doc.forms.remove(slug)
            doc.save()
        messages.add_message(self.request, messages.INFO, "Eventuele wijzigingen zijn opgeslagen.")
        return response


class GenericCaseUpdateV2FormView(GenericCaseUpdateFormView):
    template_name = 'forms/generic_form_v2.html'


class GenericCaseCreateFormView(UserPassesTestMixin, GenericCreateFormView):
    model = Case
    template_name = 'forms/generic_form.html'
    success_url = reverse_lazy('cases_by_profile')
    form_class = CaseGenericModelForm

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def get_success_url(self):
        form_context = FORMS_BY_SLUG.get(self.kwargs.get('slug'), {})
        if not form_context.get('enable_ajax', False):
            return reverse('case', kwargs={'pk': self.object.id})
        return reverse('update_case', kwargs={'pk': self.object.id, 'slug': self.kwargs.get('slug')})

    def get_discard_url(self):
        return reverse('cases_by_profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        case = form.save(commit=False)
        case.saved_by = self.request.user.profile
        case.save()
        self.request.user.profile.cases.add(case)
        messages.add_message(self.request, messages.INFO, "De cliënt '%s' is aangemaakt." % case.client_name)
        return response


class SendCaseView(UserPassesTestMixin, UpdateView):
    model = Case
    template_name = 'cases/send.html'
    form_class = SendCaseForm

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def get_success_url(self):
        return reverse('case', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        kwargs.update(self.kwargs)
        form_context = FORMS_BY_SLUG.get(self.kwargs.get('slug'))
        if not form_context:
            raise Http404
        kwargs.update(form_context)
        kwargs.update({
            'organization_list': Organization.objects.filter(main_email__isnull=False),
            'object': self.object,
            'document_list': Document.objects.filter(case=self.object, forms__contains=self.kwargs.get('slug')),
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        version = self.object.create_version(self.kwargs.get('slug'))

        case_status_dict = {
            'form': self.kwargs.get('slug'),
            'case': self.object,
            'case_version': version,
            'profile': self.request.user.profile,
        }
        case_status = CaseStatus(**case_status_dict)
        case_status.save()

        organization_list = Organization.objects.filter(main_email__isnull=False)
        for organization in organization_list:
            current_site = get_current_site(self.request)
            body = render_to_string('cases/mail/case_link.txt', {
                'case': self.object.to_dict(organization.field_restrictions),
                'form_name': FORM_TITLE_BY_SLUG.get(self.kwargs.get('slug')),
                'case_url': 'https://%s%s' % (
                    current_site.domain,
                    reverse('case_version_form', kwargs={
                        'pk': self.object.id,
                        'slug': self.kwargs.get('slug'),
                    })
                ),
                'user': self.request.user,
            })
            if settings.SENDGRID_KEY:
                sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
                email = Mail(
                    from_email='noreply@%s' % current_site.domain,
                    to_emails=organization.main_email,
                    subject='Omslagroute - %s' % FORM_TITLE_BY_SLUG.get(self.kwargs.get('slug')),
                    plain_text_content=body
                )
                sg.send(email)
            messages.add_message(
                self.request, messages.INFO, "De cliëntgegevens van '%s', zijn gestuurd naar '%s'." % (
                    self.object.client_name,
                    organization.main_email
                )
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CaseInviteUsers(UserPassesTestMixin, SessionWizardView):
    model = Case
    template_name = 'cases/case_invite.html'
    form_class = CaseInviteUsersForm
    success_url = reverse_lazy('cases_by_profile')
    instance = None
    form_list = [
        CaseInviteUsersForm,
        CaseInviteUsersConfirmForm,
    ]

    def get_success_url(self):
        return '%s?iframe=true' % reverse('case', kwargs={'pk': self.instance.id})

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step=step)
        self.instance = self.model.objects.get(id=self.kwargs.get('pk'))
        kwargs.update({
            'user': self.request.user,
            'instance': self.instance,
        })
        return kwargs

    def get_queryset(self):
        return self.request.user.profile.cases.all()

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_context_data(self, **kwargs):
        linked_users = User.objects.filter(profile__in=self.instance.profile_set.all(), user_type__in=[BEGELEIDER, PB_FEDERATIE_BEHEERDER]).exclude(id=self.request.user.id)
        kwargs.update({
            'linked_users': linked_users,
            'unlinked_users': User.objects.filter(user_type__in=[BEGELEIDER, PB_FEDERATIE_BEHEERDER]).exclude(id=self.request.user.id).exclude(id__in=linked_users.values('id')),
            'instance': self.instance,
            'selected_users': self.get_all_cleaned_data().get('user_list', []),
        })
        kwargs = super().get_context_data(**kwargs)
        return kwargs

    def done(self, form_list, **kwargs):
        form_data = {}
        for f in form_list:
            form_data.update(f.cleaned_data)

        user_list = form_data.get('user_list', [])
        for user in user_list:
            user.profile.cases.add(self.instance)
        if settings.SENDGRID_KEY:
            sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            current_site = get_current_site(self.request)
            for invited in user_list:
                context = {}
                context.update(form_data)
                context.update({
                    'case': self.instance,
                    'user': self.request.user,
                    'invited': invited,
                    'case_url': 'https://%s%s' % (
                        current_site.domain, 
                        reverse('case', kwargs={'pk':self.instance.id})
                    ),
                })
                body = render_to_string('cases/mail/invite.txt', context)
                email = Mail(
                    from_email='noreply@%s' % current_site.domain,
                    to_emails=invited.username,
                    subject='Omslagroute - je bent toegevoegd aan een team',
                    plain_text_content=body
                )
                sg.send(email)

        messages.add_message(self.request, messages.INFO, "De nieuwe gebruikers hebben een email gekregen van hun uitnodiging.")
        return HttpResponseRedirect(self.get_success_url())


class CaseRemoveInvitedUsers(UserPassesTestMixin, FormView):
    model = Case
    template_name = 'cases/case_remove_invited.html'
    form_class = CaseRemoveInvitedUsersForm
    success_url = reverse_lazy('cases_by_profile')

    def get_success_url(self):
        return '%s?iframe=true' % reverse('case', kwargs={'pk': self.instance.id})

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.instance = self.model.objects.get(id=self.kwargs.get('pk'))
        kwargs.update({
            'user': self.request.user,
            'instance': self.instance,
        })
        return kwargs

    def form_valid(self, form):
        for user in form.cleaned_data.get('user_list'):
            user.profile.cases.remove(self.instance)

        if settings.SENDGRID_KEY:
            sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            current_site = get_current_site(self.request)
            for user in form.cleaned_data.get('user_list'):
                context = {}
                context.update({
                    'case': self.instance,
                    'user': self.request.user,
                    'removed_user': user,
                    'case_url': 'https://%s%s' % (
                        current_site.domain, 
                        reverse('case', kwargs={'pk':self.instance.id})
                    ),
                })
                body = render_to_string('cases/mail/invated_removed.txt', context)
                email = Mail(
                    from_email='noreply@%s' % current_site.domain,
                    to_emails=user.username,
                    subject='Omslagroute - je bent uit een team verwijderd',
                    plain_text_content=body
                )
                sg.send(email)

        messages.add_message(self.request, messages.INFO, "De gebruikers hebben een mail ontvangen van het verbreken van de samenwerking.")
        return super().form_valid(form)



class DocumentCreate(UserPassesTestMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        if self.request.POST.get('next'):
            return '%s' % self.request.POST.get('next')
        return reverse('case', kwargs={'pk': self.kwargs.get('case_pk')})

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_context_data(self, **kwargs):
        try:
            case = self.request.user.profile.cases.get(id=self.kwargs.get('case_pk'))
        except:
            raise Http404

        kwargs.update({
            'case': case,
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        document = form.save(commit=False)
        document.case = Case.objects.get(id=self.kwargs.get('case_pk'))

        messages.add_message(self.request, messages.INFO, "De bijlage '%s' is opgeslagen." % document.name)
        return super().form_valid(form)


class DocumentUpdate(UserPassesTestMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse('case', kwargs={'pk': self.kwargs.get('case_pk')})

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_context_data(self, **kwargs):
        try:
            case = self.request.user.profile.cases.get(id=self.kwargs.get('case_pk'))
        except:
            raise Http404

        kwargs.update({
            'case': case,
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        document = form.save(commit=False)
        document.case = Case.objects.get(id=self.kwargs.get('case_pk'))

        messages.add_message(self.request, messages.INFO, "De bijlage '%s' is opgeslagen." % document.name)
        return super().form_valid(form)


class DocumentDelete(UserPassesTestMixin, DeleteView):
    model = Document
    form_class = DocumentForm
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return '%s?iframe=true' % reverse(
            'case', 
            kwargs={'pk': self.kwargs.get('case_pk')}
        )

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, PB_FEDERATIE_BEHEERDER]) and hasattr(self.request.user, 'profile')

    def get_context_data(self, **kwargs):
        try:
            case = self.request.user.profile.cases.get(id=self.kwargs.get('case_pk'))
        except:
            raise Http404

        form_status_list = [f[0] for f in case.casestatus_set.all().order_by('form').distinct().values_list('form')]

        kwargs.update({
            'case': case,
            'shared_in_forms': [f for f in self.object.forms if f in form_status_list],
        })
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        document_name = self.get_object().name
        response = super().delete(self, request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, "De bijlage '%s' is verwijderd." % document_name)
        return response


@user_passes_test(auth_test, user_type=[WONEN, BEGELEIDER, PB_FEDERATIE_BEHEERDER])
def download_document(request, case_pk, document_pk):
    if request.user.user_type in [BEGELEIDER, PB_FEDERATIE_BEHEERDER]:
        try:
            case = request.user.profile.cases.get(id=case_pk)
        except:
            raise PermissionDenied
        document = get_object_or_404(Document, id=document_pk)

    if request.user.user_type == WONEN:
        try:
            case = Case.objects.get(id=case_pk)
        except:
            raise PermissionDenied
        document = get_object_or_404(Document, id=document_pk)

        form_status_list = [f[0] for f in case.casestatus_set.all().order_by('form').distinct().values_list('form')]
        shared_in_forms = [f for f in document.forms if f in form_status_list]
        if not shared_in_forms:
            raise PermissionDenied

    if document.case != case:
        raise PermissionDenied

    if not default_storage.exists(default_storage.generate_filename(document.uploaded_file.name)):
        raise Http404()

    return HttpResponseRedirect(document.uploaded_file.url)










