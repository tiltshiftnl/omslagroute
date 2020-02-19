from django.db import models
from django.utils.translation import ugettext_lazy as _


class Document(models.Model):
    title = models.CharField(
        verbose_name=_('Titel'),
        max_length=100,
    )
    uploaded_file = models.FileField(
        verbose_name=_('Bestand'),
        upload_to='uploads'
    )
    uploaded = models.DateTimeField(
        verbose_name=_('Upload datum/tijd'),
        auto_now_add=True,
    )
    saved = models.DateTimeField(
        verbose_name=_('Opgeslagen datum/tijd'),
        auto_now=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Bestand')
        verbose_name_plural = _('Bestanden')
        ordering = ('-uploaded', )
