# Generated by Django 2.2.10 on 2020-07-17 09:40

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0024_auto_20200717_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='rol_restrictions',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Redactie'), (2, 'Wonen medewerker'), (4, 'Woningcorporatie medewerker'), (5, 'Persoonlijk begeleider'), (6, 'Onbekend/inactief'), (7, 'Beheerder'), (8, 'Organisatie beheerder'), (9, 'PB & Organisatie beheerder')], max_length=15, null=True, verbose_name='Rol opties voor federatie beheerder'),
        ),
    ]
