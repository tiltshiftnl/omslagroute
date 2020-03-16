from django.db import models
from django.utils.translation import ugettext_lazy as _
from web.core.models import PrintableModel


class Moment(PrintableModel):
    name = models.CharField(
        verbose_name=_('Naam'),
        max_length=100
    )
    description = models.TextField(
        verbose_name=_('Omschrijving van het moment'),
        blank=True,
        null=True,
    )
    order = models.IntegerField(
        verbose_name=_('Sorteer'),
        default=1,
        blank=True,
        null=True,
    )
    documents = models.ManyToManyField(
        to='documents.Document',
        verbose_name=_('Documenten'),
        blank=True,
    )
    roles = models.ManyToManyField(
        to='roles.Role',
        verbose_name=_('Rollen'),
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Moment')
        verbose_name_plural = _('Momenten')
        ordering = ('order',)
