from django.db import models
from django.utils.translation import ugettext_lazy as _


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
