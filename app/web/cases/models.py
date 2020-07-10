import os
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
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.core.files.storage import default_storage
from constance import config
from .managers import *


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
    saved_by = models.ForeignKey(
        to='profiles.Profile',
        verbose_name=_('Opgeslagen door'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    saved_form = models.CharField(
        verbose_name=_('Formulier'),
        max_length=100,
        blank=True,
        null=True,
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
    partner_check = models.PositiveSmallIntegerField(
        verbose_name=_('Heeft de cliënt een partner?'),
        choices=DEFAULT_NO_OR_YES,
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
    kinderen_check = models.PositiveSmallIntegerField(
        verbose_name=_('Heeft de cliënt kinderen?'),
        choices=DEFAULT_NO_OR_YES,
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
    medische_problemen_mbt_traplopen_check = models.PositiveSmallIntegerField(
        verbose_name=_('Zijn er medische problemen m.b.t. traplopen?'),
        choices=DEFAULT_NO_OR_YES,
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
    omklap_akkoord_derde = models.PositiveSmallIntegerField(
        verbose_name=_('Akkoord objectieve derde'),
        choices=DEFAULT_YES_OR_NO,
        blank=True,
        null=True,
    )
    omklap_akkoord_derde_toelichting = models.TextField(
        verbose_name=_('Toelichting'),
        blank=True,
        null=True,
    )
    omklap_akkoord_derde_naam = models.TextField(
        verbose_name=_('Naam / afdeling objectieve derde'),
        blank=True,
        null=True,
    )
    omklap_akkoord_derde_datum = models.DateField(
        verbose_name=_('Datum van akkoord'),
        blank=True,
        null=True,
    )
    wonen_dossier_nr = models.CharField(
        verbose_name=_('Dossier nr.'),
        max_length=100,
        blank=True,
        null=True,
    )
    adres_straatnaam = models.CharField(
        verbose_name=_('Straatnaam'),
        max_length=100,
        blank=True,
        null=True,
    )
    adres_huisnummer = models.CharField(
        verbose_name=_('Huisnummer'),
        max_length=10,
        blank=True,
        null=True,
    )
    adres_toevoeging = models.CharField(
        verbose_name=_('Toevoeging'),
        max_length=10,
        blank=True,
        null=True,
    )
    adres_postcode = models.CharField(
        verbose_name=_('Postcode'),
        max_length=10,
        blank=True,
        null=True,
    )
    adres_plaatsnaam = models.CharField(
        verbose_name=_('Plaatsnaam'),
        max_length=100,
        blank=True,
        null=True,
    )
    adres_wijziging_reden = models.TextField(
        verbose_name=_('Waarom wijzig je dit adres?'),
        blank=True,
        null=True,
    )
    woningcorporatie = models.ForeignKey(
        to='organizations.Federation',
        verbose_name=_('Woningcorporatie'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    woningcorporatie_medewerker = models.ForeignKey(
        to='profiles.Profile',
        related_name="%(app_label)s_%(class)s_set",
        verbose_name=_('Woningcorporatie medewerker'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # Kennismaking wooncorporatie
    kennismaking_wooncorporatie_goed_huurderschap = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie goed huurderschap'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_kennisgemaakt_buren = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie kennisgemaakt buren'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_kennismaken_buren = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie kennismaken buren'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_goede_buur = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie goede buur'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_huisregels = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie huisregels'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_afval = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie afval'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_technische_klachten = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie technische klachten'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_overlast_melden = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie overlast melden'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_overlast_voorkomen = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie overlast voorkomen'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_overlast_signalen = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie overlast signalen'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_wijk = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie wijk'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_wijk_voorzieningen_waar = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie_wijk voorzieningen waar'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_wijk_voorzieningen_behoefte = models.TextField(
        verbose_name=_('kennismaking_wooncorporatie_wijk_voorzieningen behoefte'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_wijk_voorzieningen_anders = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie wijk voorzieningen anders'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_doelen_wonen_huurderschap = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie doelen wonen huurderschap'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_ondersteuning_medewerker = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie ondersteuning medewerker'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_borg_betalen = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie borg betalen'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_borg_bedrag = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie borg bedrag'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_bewoner = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord bewoner'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_bewoner_naam = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord bewoner naam'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_bewoner_datum = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord bewoner datum'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_zorgaanbieder = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord zorgaanbieder'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_zorgaanbieder_naam = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord zorgaanbieder naam'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_zorgaanbieder_datum = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord zorgaanbieder datum'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_woningcorporatie = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord woningcorporatie'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_woningcorporatie_naam = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord woningcorporatie naam'),
        blank=True,
        null=True,
    )
    kennismaking_wooncorporatie_akkoord_woningcorporatie_datum = models.TextField(
        verbose_name=_('Kennismaking wooncorporatie akkoord woningcorporatie datum'),
        blank=True,
        null=True,
    )
     = models.TextField(
        verbose_name=_(''),
        blank=True,
        null=True,
    )


    @property
    def centrale_toegang_naam_value(self):
        if self.centrale_toegang_naam:
            return CENTRALE_TOEGANG_DICT[self.centrale_toegang_naam]
        return self.EMPTY_VALUE

    @property
    def woningcorporatie_akkoord_met_omklap_value(self):
        if self.woningcorporatie_akkoord_met_omklap:
            return DEFAULT_YES_OR_NO_DICT[self.woningcorporatie_akkoord_met_omklap]
        return self.EMPTY_VALUE

    @property
    def urgentiecriteria_zinvolle_dagbesteding_akkoord_value(self):
        if self.urgentiecriteria_zinvolle_dagbesteding_akkoord:
            return DEFAULT_YES_OR_NO_DICT[self.urgentiecriteria_zinvolle_dagbesteding_akkoord]
        return self.EMPTY_VALUE

    @property
    def urgentiecriteria_functioneert_psychisch_akkoord_value(self):
        if self.urgentiecriteria_functioneert_psychisch_akkoord:
            return DEFAULT_YES_OR_NO_DICT[self.urgentiecriteria_functioneert_psychisch_akkoord]
        return self.EMPTY_VALUE

    @property
    def urgentiecriteria_is_financieel_stabiel_akkoord_value(self):
        if self.urgentiecriteria_is_financieel_stabiel_akkoord:
            return DEFAULT_YES_OR_NO_DICT[self.urgentiecriteria_is_financieel_stabiel_akkoord]
        return self.EMPTY_VALUE

    @property
    def urgentiecriteria_functioneert_sociaal_akkoord_value(self):
        if self.urgentiecriteria_functioneert_sociaal_akkoord:
            return DEFAULT_YES_OR_NO_DICT[self.urgentiecriteria_functioneert_sociaal_akkoord]
        return self.EMPTY_VALUE

    @property
    def urgentiecriteria_kinderen_gezonde_akkoord_value(self):
        if self.urgentiecriteria_kinderen_gezonde_akkoord:
            return DEFAULT_YES_OR_NO_DICT[self.urgentiecriteria_kinderen_gezonde_akkoord]
        return self.EMPTY_VALUE

    @property
    def partner_check_value(self):
        if self.partner_check:
            return DEFAULT_NO_OR_YES_DICT[self.partner_check]
        return self.EMPTY_VALUE

    @property
    def kinderen_check_value(self):
        if self.kinderen_check:
            return DEFAULT_NO_OR_YES_DICT[self.kinderen_check]
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

    @property
    def address_complete(self):
        return bool(
            self.adres_straatnaam and self.adres_huisnummer and self.adres_postcode and self.adres_plaatsnaam
        ) 

    def __str__(self):
        if self.client_first_name:
            return self.client_first_name
        if self.client_last_name:
            return self.client_last_name
        return '%s' % self.id

    class Meta:
        abstract = True


class Case(CaseBase):
    delete_request_date = models.DateTimeField(
        verbose_name=_('Verwijder verzoek datum'),
        blank=True,
        null=True,
    )
    delete_request_by = models.ForeignKey(
        to='profiles.Profile',
        related_name='profile_list',
        verbose_name=_('Verwijder verzoek door'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    delete_request_message = models.TextField(
        verbose_name=_('Verwijder verzoek bericht'),
        blank=True,
        null=True,
    )
    objects = CaseManager()

    @property
    def is_ingediend(self):
        return bool(CaseVersion.objects.filter(case=self))

    @property
    def delete_request_seconds_left(self):
        from datetime import datetime
        datetime_treshold = datetime.now() - timedelta(seconds=config.CASE_DELETE_SECONDS)
        time_left = self.delete_request_date - datetime_treshold
        return time_left

    def delete_enabled(self):
        datetime_treshold = datetime.now() - timedelta(seconds=config.CASE_DELETE_SECONDS)
        time_left = self.delete_request_date - datetime_treshold
        return time_left.total_seconds() <= 0

    def create_version(self, version):
        case_dict = dict(
            (ff.name, getattr(self, ff.name)) for ff in Case._meta.get_fields()
            if hasattr(self, ff.name) and ff.name in [f.name for f in CaseVersion._meta.get_fields()]
        )
        case_version = CaseVersion(**case_dict)
        case_version.pk = None
        case_version.id = None
        case_version.version_verbose = version
        case_version.case = self
        case_version.save()
        return case_version

    def delete_related(self):
        document_path = os.path.join(
            'uploads',
            'cases',
            '%a' % self.id
        )
        if default_storage.exists(document_path):
            dirs, files = default_storage.listdir(document_path)
            for f in files:
                file_path = os.path.join(
                    document_path,
                    f
                )
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
            default_storage.delete(document_path)

        CaseVersion.objects.filter(case=self).delete()
        CaseStatus.objects.filter(case=self).delete()
        Document.objects.filter(case=self).delete()
        return True

    def get_history(self, version=None, double_values=True):
        qs = self.case_version_list.all().order_by('-saved')
        if isinstance(version, list):
            qs = qs.filter(version_verbose__in=version)
        value_key = 'value'
        version_key = 'version_verbose'
        saved_key = 'saved'
        object_dict = self.to_dict()
        ld = [cv.to_dict() for cv in qs]
        ld = ld if ld else [{}]
        dl = {k: [{
            value_key: dic[k].get('value'),
            version_key: CASE_VERSION_BY_SLUG.get(dic[version_key].get('value'), {}).get('title'),
            saved_key: dic[saved_key].get('value'),
        } for dic in ld] for k in ld[0] if object_dict.get(k)}
        if double_values:
            dl = {k: [
                vv for vv in v if vv.get(value_key) != '—' and vv.get(value_key) != object_dict.get(k, {}).get('value')
            ] for k, v in dl.items()}
            # remove double values
            dl = {k: [
                v[i] for i in range(len(v)) if i == 0 or v[i].get('value') != v[i-1].get('value')
            ] for k, v in dl.items()}
        return dl

    def delete(self):
        deleted = self.delete_related()
        if deleted:
            super().delete()
        return False

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


class CaseStatus(models.Model):
    status = models.SmallIntegerField(
        verbose_name=_('Status'),
        choices=CASE_STATUS_CHOICES,
        default=CASE_STATUS_CHOICES[0][0],
    )
    status_comment = models.TextField(
        verbose_name=_('Opmerking'),
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        verbose_name=_('Initieel opgeslagen datum/tijd'),
        auto_now_add=True,
    )
    form = models.CharField(
        verbose_name=_('Formulier'),
        max_length=100,
        blank=True,
        null=True,
    )
    case = models.ForeignKey(
        to='Case',
        verbose_name=_('Cliënt'),
        on_delete=models.CASCADE,
    )
    case_version = models.ForeignKey(
        to='CaseVersion',
        verbose_name=_('Cliënt versie'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    profile = models.ForeignKey(
        to='profiles.Profile',
        on_delete=models.CASCADE,
        verbose_name=_('Profiel'),
        blank=True,
        null=True,
    )

    @property
    def is_first_of_statustype(self):
        return CaseStatus.objects.filter(
            case=self.case, 
            status=self.status, 
            form=self.form, 
        ).count() <= 1

    def __str__(self):
        return self.html()

    def html(self):
        locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")
        return mark_safe('<div><span>%s</span><small>%s</small><small>%s</small></div>' % (
                self.case.id,
                self.form,
                self.created.strftime('%d %b %Y %H:%M:%S').lower()
            )
        )

    @property
    def case_form_is_opnieuw_ingediend(self):
        status_list = CaseStatus.objects.order_by('-created')
        status_list = status_list.filter(
                form=self.form, 
                case=self.case
        )
        first = status_list.first()
        return first.status == 1 if first else False
        
    class Meta:
        verbose_name = _('Cliënt status')
        verbose_name_plural = _('Cliënt statussen')
        ordering = ('-created', 'case', 'form')


def get_upload_path(instance, filename):
    return os.path.join(
      "uploads", 'cases', '%s' % instance.case.id, filename)


class Document(models.Model):
    name = models.CharField(
        verbose_name=_('Titel van het document'),
        max_length=100,
    )
    uploaded_file = models.FileField(
        verbose_name=_('Selecteer een bestand'),
        upload_to=get_upload_path
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
        timezone.activate(settings.FRONTEND_TIMEZONE)
        return mark_safe('<div><span><a href=%s target="_blank">%s</a></span><small>%s</small><small>%s</small></div>' % (
                reverse('download_case_document', args=[self.case.id, self.id]),
                self.name,
                self.extension,
                timezone.localtime(self.uploaded).strftime('%d %b %Y %H:%M:%S').lower() if timezone.is_aware(self.uploaded) else self.uploaded.strftime('%d %b %Y %H:%M:%S').lower()
            )
        )
        timezone.deactivate()

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
