from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        to='users.User',
        verbose_name=_('Gebruiker'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    cases = models.ManyToManyField(
        to='cases.Case',
        verbose_name=_('Cliënten'),
        blank=True,
    )
    organization = models.ForeignKey(
        to='organizations.Organization',
        verbose_name=_('Organisatie'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.user:
            return self.user.username
        return self.id
