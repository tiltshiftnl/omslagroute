from django.db import models
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from web.cases.models import Case
from web.users.models import User


def get_fields():
    return [[str(f.name), '%s [%s]' % (
        str(f.name),
        str(f.verbose_name),
    )] for f in Case._meta.fields]


class Organization(models.Model):
    name = models.CharField(
        verbose_name=_('Naam'),
        max_length=100
    )
    name_abbreviation = models.CharField(
        verbose_name=_('Naam afkorting'),
        max_length=4,
        blank=True,
        null=True,
    )
    main_email = models.EmailField(
        verbose_name=('Standaard e-mailadres'),
        max_length=100,
        blank=True,
        null=True,
    )
    field_restrictions = MultiSelectField(
        verbose_name=_('Cliënt gegevens velden'),
        help_text=_('De inhoud van een geselecteerd veld wordt zichtbaar voor deze organisatie.'),
        choices=get_fields(),
        blank=True,
        null=True,
    )
    rol_restrictions = MultiSelectField(
        verbose_name=_('Rol opties voor federatie beheerder'),
        choices=User.user_types,
        blank=True,
        null=True,
    )

    def get_case_data(self, case):
        return case.to_dict(self.field_restrictions)

    @property
    def abbreviation(self):
        if self.name_abbreviation:
            return self.name_abbreviation
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Organisatie')
        verbose_name_plural = _('Organisaties')
        ordering = ('name',)


class Federation(models.Model):
    name = models.CharField(
        verbose_name=_('Naam'),
        max_length=100,
    )
    federation_id = models.CharField(
        verbose_name=_('Federatie id'),
        max_length=100,
        unique=True,
    )
    name_abbreviation = models.CharField(
        verbose_name=_('Naam afkorting'),
        max_length=4,
        blank=True,
        null=True,
    )
    main_email = models.EmailField(
        verbose_name=('Standaard e-mailadres'),
        max_length=100,
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        to='Organization',
        verbose_name=('Organisatie'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    @property
    def abbreviation(self):
        if self.name_abbreviation:
            return self.name_abbreviation
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Federatie')
        verbose_name_plural = _('Federaties')
        ordering = ('name',)
