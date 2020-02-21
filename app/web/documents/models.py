from django.db import models
from django.utils.translation import ugettext_lazy as _
from .statics import ICON_LIST


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        to='Document',
        verbose_name='Document',
        related_name='document_to_document_version',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    uploaded_file = models.FileField(
        verbose_name=_('Bestand'),
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

    def __str__(self):
        if self.document:
            return self.document.name
        return self.uploaded.strftime('Y-M-d')

    class Meta:
        verbose_name = _('Document versie')
        verbose_name_plural = _('Document versies')
        ordering = ('-uploaded', )


class Document(models.Model):
    name = models.CharField(
        verbose_name=_('Type naam'),
        max_length=100,
    )
    icon = models.CharField(
        verbose_name=_('Icon'),
        max_length=50,
        choices=ICON_LIST,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documenten')
        ordering = ('name', )

    @property
    def icon_path(self):
        return 'images/%s.svg' % self.icon

    def __str__(self):
        return self.name
