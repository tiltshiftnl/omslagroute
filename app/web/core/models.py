from django.db import models
from django.db.models.fields.related import ManyToManyField
import datetime
from textile import textile
import json
from django.core.files import File


class PrintableModel(models.Model):
    def to_dict(self, fields=None):
        opts = self._meta
        textile_fields = getattr(self.__class__, 'textile_fields') if hasattr(self.__class__, 'textile_fields') else []
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if fields is None or f.name in fields:
                if hasattr(self, '%s_value' % f.name):
                    data[f.name] = getattr(self, '%s_value' % f.name)
                elif isinstance(f, ManyToManyField):
                    if self.pk is None:
                        data[f.name] = []
                    else:
                        data[f.name] = [v.pk for v in f.value_from_object(self)]
                elif isinstance(f, models.DateTimeField):
                    if f.value_from_object(self) is not None:
                        data[f.name] = f.value_from_object(self).timestamp()
                    else:
                        data[f.name] = None
                elif isinstance(f, models.BooleanField):
                    data[f.name] = 'Ja' if f.value_from_object(self) else 'Nee'
                else:
                    data[f.name] = f.value_from_object(self)
                if isinstance(data[f.name], File):
                    try:
                        data[f.name] = data[f.name].url
                    except:
                        data[f.name] = '-'

                if isinstance(data[f.name], datetime.date):
                    data[f.name] = datetime.datetime.strftime(data[f.name], '%d-%m-%Y')
                if isinstance(data[f.name], datetime.datetime):
                    data[f.name] = data[f.name].isoformat()
                if data[f.name] is None or data[f.name] is '':
                    data[f.name] = self.EMPTY_VALUE if hasattr(self, 'EMPTY_VALUE') else '\u2014'
                if f.name in textile_fields:
                    data[f.name] = textile(data[f.name])
                data[f.name] = {
                    'value': data[f.name],
                    'label': str(f.verbose_name)
                }
        return data

    class Meta:
        abstract = True
