from django.db import models
from django.utils.translation import ugettext_lazy as _
from .statics import ICON_LIST, ICON_DICT


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

    def __str__(self):
        if self.document:
            return self.document.name
        return self.uploaded.strftime('%Y-%m-%d, %H:%M:%S')

    @property
    def uploaded_str(self):
        return self.uploaded.strftime('%Y-%m-%d, %H:%M:%S')

    class Meta:
        verbose_name = _('Document versie')
        verbose_name_plural = _('Document versies')
        ordering = ('-uploaded', )


class Document(models.Model):
    name = models.CharField(
        verbose_name=_('Titel van het document'),
        max_length=100,
        unique=True,
    )
    icon = models.CharField(
        verbose_name=_('Documenttype'),
        max_length=50,
        default='form',
        choices=ICON_LIST,
    )

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documenten')
        ordering = ('name', )

    @property
    def icon_path(self):
        return 'images/%s.svg' % self.icon

    @property
    def icon_value(self):
        return ICON_DICT.get(self.icon)

    def __str__(self):
        return self.name
