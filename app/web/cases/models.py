from django.db import models
from django.utils.translation import ugettext_lazy as _


class Case(models.Model):
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

    @property
    def client_name(self):
        if self.client_first_name or self.client_last_name:
            return '%s %s' % (self.client_first_name, self.client_last_name)
        return str(self.id)

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
