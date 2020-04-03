from django.db import models
from django.utils.translation import ugettext_lazy as _
from .statics import *
from web.core.models import PrintableModel
from web.forms.forms import BaseGenericForm
from web.forms.statics import FIELDS_DICT


class Case(PrintableModel):
    EMPTY_VALUE = '- leeg -'

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
        print(section_fields)
        required_fields = [f for f in section_fields if FIELDS_DICT.get(f) and FIELDS_DICT.get(f).required]
        print(required_fields)
        filled_fields = [f for f in required_fields if hasattr(self, f) and getattr(self, f)]
        return int(float(float(len(filled_fields) / len(required_fields))) * 100)

    def __str__(self):
        if self.client_first_name:
            return self.client_first_name
        if self.client_last_name:
            return self.client_last_name
        return self.id

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clienten')
        ordering = ('client_last_name', )
