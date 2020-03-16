from django.db import models
from django.db.models.fields.related import ManyToManyField


class PrintableModel(models.Model):

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = [v.__str__() for v in f.value_from_object(self)]
            elif isinstance(f, models.DateTimeField):
                if f.value_from_object(self) is not None:
                    data[f.name] = f.value_from_object(self).timestamp()
                else:
                    data[f.name] = None
            else:
                data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        abstract = True
