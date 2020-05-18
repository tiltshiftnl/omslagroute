from django.db import models
from django.utils.translation import ugettext_lazy as _
from .statics import *
from web.core.models import PrintableModel
from web.forms.forms import BaseGenericForm
from web.forms.statics import FIELDS_DICT, FIELDS_REQUIRED_DICT, FORMS_PROCESSTAP_CHOICES
import os
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe
import locale


class CaseBase(PrintableModel):
    EMPTY_VALUE = '\u2014'

    created = models.DateTimeField(
        verbose_name=_('Initieel opgeslagen datum/tijd'),
        auto_now_add=True,
    )
    saved = models.DateTimeField(
        verbose_name=_('Opgeslagen datum/tijd'),
        auto_now=True,
    )
    client_first_name = models.CharField(
        verbose_name=_('Client voornaam'),
        max_length=100,
        blank=True,
        null=True,
    )
    client_last_name = models.CharField(
        max_length=100,
        verbose_name=_('Client achternaam'),
        blank=True,
        null=True,
    )
    geslacht = models.PositiveSmallIntegerField(
        verbose_name=_('Geslacht'),
        choices=GESLACHT,
        blank=True,
        null=True,
    )
    geboortedatum = models.DateField(
        verbose_name=_('Geboortedatum'),
        blank=True,
        null=True,
    )
    emailadres = models.EmailField(
        verbose_name=_('E-mailadres'),
        blank=True,
        null=True,
    )
    woningnet_nummer = models.CharField(
        max_length=50,
        verbose_name=_('Woningnetnummer'),
        blank=True,
        null=True,
    )
    woningnet_geldigheid = models.DateField(
        verbose_name=_('Geldigheid woninget'),
        blank=True,
        null=True,
    )
    centrale_toegang_naam = models.PositiveSmallIntegerField(
        verbose_name=_('Naam centrale toegang'),
        choices=CENTRALE_TOEGANG,
        blank=True,
        null=True,
    )
    jonger_dan_26 = models.PositiveSmallIntegerField(
        verbose_name=_('Plaatsing jonger dan 26 jaar'),
        choices=JONGER_DAN_26,
        blank=True,
        null=True,
    )
    jonger_dan_26_plaatsing_project = models.TextField(
        verbose_name=_('Plaatsing jonger project'),
        blank=True,
        null=True,
    )
    jonger_dan_26_motivatie_contract_onbepaalde = models.TextField(
        verbose_name=_('Motivatie voor contract onbepaalde tijd jongere'),
        blank=True,
        null=True,
    )
    partner_naam = models.CharField(
        verbose_name=_('Partner naam'),
        max_length=100,
        blank=True,
        null=True,
    )
    partner_geboortedatum = models.DateField(
        verbose_name=_('Partner geboortedatum'),
        blank=True,
        null=True,
    )
    partner_gehuwd = models.BooleanField(
        verbose_name=_('Gehuwd?'),
        blank=True,
        null=True,
    )
    partner_echtscheiding_rond = models.BooleanField(
        verbose_name=_('Echtscheiding rond?'),
        blank=True,
        null=True,
    )
    partner_woonsituatie = models.TextField(
        verbose_name=_('Woonsituatie partner'),
        blank=True,
        null=True,
    )
    kinderen = models.TextField(
        verbose_name=_('Kinderen'),
        blank=True,
        null=True,
    )
    centrale_toegang_trajectwijziging_ed = models.PositiveSmallIntegerField(
        verbose_name=_('Toegang en trajectwijziging / doorstroom en jeugdzorg'),
        choices=CENTRALE_TOEGANG,
        blank=True,
        null=True,
    )
    trajecthouder_naam = models.CharField(
        verbose_name=_('Naam instroomfunctionaris of trajecthouder'),
        max_length=100,
        blank=True,
        null=True,
    )
    aanvraag_datum = models.DateField(
        verbose_name=_('Datum aanvraag'),
        blank=True,
        null=True,
    )
    omslagwoning_zorgaanbieder = models.CharField(
        verbose_name=_('Zorgaanbieder omslagwoning'),
        max_length=100,
        blank=True,
        null=True,
    )
    urgentiecriteria_zinvolle_dagbesteding = models.TextField(
        verbose_name=_('De cliënt heeft passende zinvolle dagbesteding'),
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_sociaal_stabiel = models.TextField(
        verbose_name=_('De cliënt functioneert sociaal stabiel'),
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_psychisch_stabiel = models.TextField(
        verbose_name=_('De cliënt functioneert psychisch stabiel'),
        blank=True,
        null=True,
    )
    urgentiecriteria_is_financieel_stabiel = models.TextField(
        verbose_name=_('De cliënt is financieel stabiel'),
        blank=True,
        null=True,
    )
    urgentiecriteria_kinderen_gezonde_omgeving = models.TextField(
        verbose_name=_('De betrokken kinderen hebben een gezonde omgeving'),
        blank=True,
        null=True,
    )
    medische_problemen_mbt_traplopen = models.BooleanField(
        verbose_name=_('Zijn er medische problemen m.b.t. traplopen?'),
        blank=True,
        null=True,
    )
    medische_problemen_wooneisen = models.TextField(
        verbose_name=_('Zo ja, benedenwoning of woning met lift? Anders?'),
        blank=True,
        null=True,
    )
    medische_problemen_bewijslast = models.FileField(
        verbose_name=_('Voeg medische gegevens toe m.b.t. problematiek'),
        blank=True,
        null=True,
    )
    uitsluiting_stadsdeel_argumentatie = models.TextField(
        verbose_name=_('Uitsluiting stadsdeel, argumentatie'),
        blank=True,
        null=True,
    )
    # omklap form
    organisatie = models.CharField(
        verbose_name=_('Organisatie'),
        max_length=100,
        blank=True,
        null=True,
    )
    persoonlijk_begeleider = models.CharField(
        verbose_name=_('Persoonlijk begeleider'),
        max_length=100,
        blank=True,
        null=True,
    )
    start_zelfstandig_wonen = models.CharField(
        verbose_name=_('Start zelfstandig wonen (intermediair)'),
        max_length=100,
        blank=True,
        null=True,
    )
    datum_voordracht = models.DateField(
        verbose_name=_('Datum voordracht'),
        blank=True,
        null=True,
    )
    woningcorporatie_akkoord_met_omklap = models.PositiveSmallIntegerField(
        verbose_name=_('Woningcorporatie akkoord met omklap'),
        choices=DEFAULT_YES_OR_NO,
        blank=True,
        null=True,
    )
    datum_evaluatie_moment = models.DateField(
        verbose_name=_('Datum evaluatie moment'),
        blank=True,
        null=True,
    )
    urgentiecriteria_zinvolle_dagbesteding_behaald_omdat = models.TextField(
        verbose_name=_('Deze doelen zijn behaald omdat'),
        blank=True,
        null=True,
    )
    urgentiecriteria_zinvolle_dagbesteding_beoordeeld_door = models.TextField(
        verbose_name=_('Deze doelen zijn beoordeeld door'),
        blank=True,
        null=True,
    )
    urgentiecriteria_zinvolle_dagbesteding_akkoord = models.PositiveSmallIntegerField(
        verbose_name=_('Akkoord'),
        choices=DEFAULT_YES_OR_NO,
        blank=True,
        null=True,
    )
    urgentiecriteria_zinvolle_dagbesteding_datum_evaluatiemoment = models.DateField(
        verbose_name=_('Datum evaluatiemoment'),
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_sociaal_behaald_omdat = models.TextField(
        verbose_name=_('Deze doelen zijn behaald omdat'),
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_sociaal_beoordeeld_door = models.TextField(
        verbose_name=_('Deze doelen zijn beoordeeld door'),
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_sociaal_akkoord = models.PositiveSmallIntegerField(
        verbose_name=_('Akkoord'),
        choices=DEFAULT_YES_OR_NO,
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_sociaal_datum_evaluatiemoment = models.DateField(
        verbose_name=_('Datum evaluatiemoment'),
        blank=True,
        null=True,
    )

    urgentiecriteria_functioneert_psychisch_behaald_omdat = models.TextField(
        verbose_name=_('Deze doelen zijn behaald omdat'),
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_psychisch_beoordeeld_door = models.TextField(
        verbose_name=_('Deze doelen zijn beoordeeld door'),
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_psychisch_akkoord = models.PositiveSmallIntegerField(
        verbose_name=_('Akkoord'),
        choices=DEFAULT_YES_OR_NO,
        blank=True,
        null=True,
    )
    urgentiecriteria_functioneert_psychisch_datum_evaluatiemoment = models.DateField(
        verbose_name=_('Datum evaluatiemoment'),
        blank=True,
        null=True,
    )

    urgentiecriteria_is_financieel_stabiel_behaald_omdat = models.TextField(
        verbose_name=_('Deze doelen zijn behaald omdat'),
        blank=True,
        null=True,
    )
    urgentiecriteria_is_financieel_stabiel_beoordeeld_door = models.TextField(
        verbose_name=_('Deze doelen zijn beoordeeld door'),
        blank=True,
        null=True,
    )
    urgentiecriteria_is_financieel_stabiel_akkoord = models.PositiveSmallIntegerField(
        verbose_name=_('Akkoord'),
        choices=DEFAULT_YES_OR_NO,
        blank=True,
        null=True,
    )
    urgentiecriteria_is_financieel_stabiel_datum_evaluatiemoment = models.DateField(
        verbose_name=_('Datum evaluatiemoment'),
        blank=True,
        null=True,
    )

    urgentiecriteria_kinderen_gezonde_behaald_omdat = models.TextField(
        verbose_name=_('Deze doelen zijn behaald omdat'),
        blank=True,
        null=True,
    )
    urgentiecriteria_kinderen_gezonde_beoordeeld_door = models.TextField(
        verbose_name=_('Deze doelen zijn beoordeeld door'),
        blank=True,
        null=True,
    )
    urgentiecriteria_kinderen_gezonde_akkoord = models.PositiveSmallIntegerField(
        verbose_name=_('Akkoord'),
        choices=DEFAULT_YES_OR_NO,
        blank=True,
        null=True,
    )
    urgentiecriteria_kinderen_gezonde_datum_evaluatiemoment = models.DateField(
        verbose_name=_('Datum evaluatiemoment'),
        blank=True,
        null=True,
    )

    omklap_client_openstaande_vragen = models.TextField(
        verbose_name=_('Voor deze cliënt staan de volgende vragen nog open'),
        blank=True,
        null=True,
    )
    omklap_client_volgende_stappen_gezet = models.TextField(
        verbose_name=_('Hiervoor worden de volgende stappen gezet (zowel formeel als informeel)'),
        blank=True,
        null=True,
    )
    omklap_beoordeeld_door = models.TextField(
        verbose_name=_('Dit is beoordeeld door'),
        blank=True,
        null=True,
    )
    omklap_datum_evaluatiemoment = models.DateField(
        verbose_name=_('Datum evaluatiemoment'),
        blank=True,
        null=True,
    )
    omklap_toelichting = models.TextField(
        verbose_name=_('Toelichting (bv. doelen niet behaald maar geen risico voor zelfstandig wonen)'),
        blank=True,
        null=True,
    )

    @property
    def centrale_toegang_naam_value(self):
        if self.centrale_toegang_naam:
            return CENTRALE_TOEGANG_DICT[self.centrale_toegang_naam]
        return self.EMPTY_VALUE

    @property
    def jonger_dan_26_value(self):
        if self.jonger_dan_26:
            return JONGER_DAN_26_DICT[self.jonger_dan_26]
        return self.EMPTY_VALUE

    @property
    def centrale_toegang_trajectwijziging_ed_value(self):
        if self.centrale_toegang_trajectwijziging_ed:
            return CENTRALE_TOEGANG_DICT[self.centrale_toegang_trajectwijziging_ed]
        return self.EMPTY_VALUE

    @property
    def geslacht_value(self):
        if self.geslacht:
            return GESLACHT_DICT[self.geslacht]
        return self.EMPTY_VALUE

    @property
    def client_name(self):
        if self.client_first_name or self.client_last_name:
            return '%s %s' % (self.client_first_name, self.client_last_name)
        return str(self.id)

    def status(self, sections):
        section_fields = BaseGenericForm._get_fields(sections)
        required_fields = [f for f in section_fields if FIELDS_REQUIRED_DICT.get(f)]
        filled_fields = [f for f in required_fields if hasattr(self, f) and getattr(self, f)]
        not_filled_fields = [FIELDS_DICT.get(f).label for f in required_fields if hasattr(self, f) and not getattr(self, f)]
        return {
            'percentage': int(float(float(len(filled_fields) / len(required_fields))) * 100),
            'remaining_fields': not_filled_fields
        }

    def __str__(self):
        if self.client_first_name:
            return self.client_first_name
        if self.client_last_name:
            return self.client_last_name
        return '%s' % self.id

    class Meta:
        abstract = True


class Case(CaseBase):
    def create_version(self, version):
        case_dict = dict(
            (k, v) for k, v in self.__dict__.items()
            if k not in ['_state']
        )
        case_version = CaseVersion(**case_dict)
        case_version.pk = None
        case_version.id = None
        case_version.version_verbose = version
        case_version.case = self
        case_version.save()
        return case_version

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clienten')
        ordering = ('client_last_name', )
        abstract = False


class CaseVersion(CaseBase):
    version_verbose = models.CharField(
        verbose_name=_('Versie'),
        max_length=100,
        blank=True,
        null=True,
    )
    case = models.ForeignKey(
        to='Case',
        related_name='case_version_list',
        verbose_name=_('Cliënt'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Client versie')
        verbose_name_plural = _('Client versies')
        ordering = ('created', )
        abstract = False


class Document(models.Model):
    name = models.CharField(
        verbose_name=_('Titel van het document'),
        max_length=100,
    )
    uploaded_file = models.FileField(
        verbose_name=_('Selecteer een bestand'),
        upload_to='uploads'
    )
    uploaded = models.DateTimeField(
        verbose_name=_('Initieel opgeslagen datum/tijd'),
        auto_now_add=True,
    )
    saved = models.DateTimeField(
        verbose_name=_('Opgeslagen datum/tijd'),
        auto_now=True,
    )
    case = models.ForeignKey(
        to='cases.Case',
        verbose_name=_('Cliënt'),
        on_delete=models.CASCADE,
    )
    forms = MultiSelectField(
        verbose_name=_('Formulieren'),
        choices=FORMS_PROCESSTAP_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")
        return mark_safe('<div><span>%s</span><small>%s</small><small>%s</small></div>' % (
                self.name,
                self.extension,
                self.saved.strftime('%d %b %Y %H:%M:%S').lower()
            )
        )

    @property
    def extension(self):
        name, extension = os.path.splitext(self.uploaded_file.name)
        return extension

    @property
    def uploaded_str(self):
        return self.uploaded.strftime('%Y-%m-%d, %H:%M:%S')

    class Meta:
        verbose_name = _('Bijlage')
        verbose_name_plural = _('Bijlagen')
        ordering = ('-uploaded', )
