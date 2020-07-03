from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import widgets
from .utils import *
from .widgets import *
from web.cases.statics import *
# from web.cases.models import Document


FIELDS = (
    ('client_first_name', forms.CharField(
        label=_('Voornaam'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=True
    ), {'step_required': True}),
    ('client_last_name', forms.CharField(
        label=_('Achternaam'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=True
    ), {'step_required': True}),
    ('geslacht', forms.ChoiceField(
        label=_('Geslacht'),
        required=False,
        widget=RadioSelect(),
        choices=GESLACHT,
    ), {}),
    ('geboortedatum', forms.DateField(
        label=_('Geboortedatum'),
        required=True,
        localize=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {}),
    ('emailadres', forms.EmailField(
        label=_('E-mailadres'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {}),
    ('woningnet_nummer', forms.CharField(
        label=_('Woningnetnummer *'),
        widget=forms.TextInput(attrs={'placeholder': ' ', 'pattern': '^[0-9]*$'}),
        required=False,
    ), {'step_required': True}),
    ('woningnet_geldigheid', forms.DateField(
        label=_('Geldigheid woningnet *'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
        help_text=_('Deze moet in de toekomst liggen')
    ), {'step_required': True}),
    ('centrale_toegang_naam', forms.IntegerField(
        label=_('Naam centrale toegang *'),
        widget=RadioSelect(
            choices=CENTRALE_TOEGANG,
        ),
        required=False,
    ), {'step_required': True}),
    ('jonger_dan_26', forms.IntegerField(
        label=_('Plaatsing jonger dan 27 jaar *'),
        widget=RadioSelect(
            choices=JONGER_DAN_26,
        ),
        required=False,
    ), {'step_required': True}),
    ('jonger_dan_26_plaatsing_project', forms.CharField(
        label=_('In geval van plaatsing in een project'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Vul naam van project in'
    ), {}),
    ('jonger_dan_26_motivatie_contract_onbepaalde', forms.CharField(
        label=_('In geval van plaatsing reguliere woning'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Wat is de motivatie voor aanvraag van een huurcontract voor onbepaalde tijd?'
    ), {}),
    ('partner_check', forms.IntegerField(
        label=_('Heeft de cliënt een partner? *'),
        widget=RadioSelect(
            choices=DEFAULT_NO_OR_YES,
        ),
        required=False,
    ), {'step_required': True}),
    ('partner_naam', forms.CharField(
        label=_('Naam partner'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {}),
    ('partner_geboortedatum', forms.DateField(
        label=_('Geboortedatum partner'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {}),
    ('partner_gehuwd', forms.BooleanField(
        label=_('Gehuwd'),
        required=False,
    ), {}),
    ('partner_echtscheiding_rond', forms.BooleanField(
        label=_('Echtscheiding rond'),
        required=False,
    ), {}),
    ('partner_woonsituatie', forms.CharField(
        label=_('Woonsituatie partner'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
        help_text='Waar/bij wie/hoe?'
    ), {}),
    ('kinderen_check', forms.IntegerField(
        label=_('Heeft de cliënt kinderen? *'),
        widget=RadioSelect(
            choices=DEFAULT_NO_OR_YES,
        ),
        required=False,
    ), {'step_required': True}),
    ('kinderen', forms.CharField(
        label=_('Kinderen'),
        help_text=_('Geef aan per kind: <ul><li>Naam + voorletters</li><li>Geboortedatum (dag-maand-jaar)</li><li>Ouderlijk gezag (ja of nee)</li><li>Mee aangemeld (ja of nee)</li></ul>'),
        widget=forms.Textarea(),
        required=False,
    ), {}),
    ('centrale_toegang_trajectwijziging_ed', forms.IntegerField(
        label=_('Toegang en trajectwijziging / doorstroom en jeugdzorg'),
        widget=RadioSelect(
            choices=CENTRALE_TOEGANG,
        ),
        required=False,
    ), {}),
    ('trajecthouder_naam', forms.CharField(
        label=_('Naam instroomfunctionaris of trajecthouder *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('aanvraag_datum', forms.DateField(
        label=_('Datum aanvraag *'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('omslagwoning_zorgaanbieder', forms.CharField(
        label=_('Zorgaanbieder omslagwoning *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding', forms.CharField(
        label=_('De cliënt heeft passende zinvolle dagbesteding. Dat betekent voor deze cliënt het volgende *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Bijvoorbeeld: cliënt wil een betaalde baan die zij kan combineren met de zorg voor haar kinderen',
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_stabiel', forms.CharField(
        label=_('De cliënt functioneert sociaal stabiel. Dat betekent voor deze cliënt het volgende *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Bijvoorbeeld: Het doel is om het huidige netwerk te behouden en het contact met haar ex-man te stabiliseren.',
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_stabiel', forms.CharField(
        label=_('De cliënt functioneert psychisch stabiel. Dat betekent voor deze cliënt het volgende *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Bijvoorbeeld: cliënt functioneert psychisch stabiel en heeft als doel dit voort te zetten. <br /><strong>Let op! Leg geen medische informatie vast.</strong>',
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel', forms.CharField(
        label=_('De cliënt is financieel stabiel. Dat betekent voor deze cliënt het volgende *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Met financieel stabiel wordt bedoeld dat deze een stabiel inkomen heeft inzage heeft gegeven in eventuele schulden op basis van informatie van Bureau KredietRegistratie.<br /><br />In het geval er schulden zijn is de cliënt financieel stabiel wanneer de cliënt aan een of meerdere van deze zaken voldoet: <ul><li>een overzicht heeft gegeven van alle schulden en betalingsverplichtingen</li><li>inzicht heeft gegeven in eventuele openstaande CJIB-boetes en heeft aangetoond dat er geen kans is op detentie vanwege openstaande boetes</li><li>in inkomensbeheer zit</li><li>een stabiel werkend budgetplan heeft</li><li>een overeenkomst heeft met een schuldhulpverleningsbureau waarbij het schuldhulpverleningstraject voorspoedig loopt</li></ul>Bijvoorbeeld: cliënt wil zelfstandig haar administratie bijhouden en haar schulden regelen.',
    ), {'step_required': True}),
    ('urgentiecriteria_kinderen_gezonde_omgeving', forms.CharField(
        label=_('De betrokken kinderen hebben een gezonde omgeving. Dat betekent voor deze cliënt het volgende:'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='De betrokken kinderen hebben een gezonde omgeving, waarmee wordt bedoeld dat deze:<ul><li>Een veilige omgeving hebben waarin zij opgroeien; en</li><li>Zich leeftijdsadequaat kunnen ontwikkelen; en</li><li>Een omgeving hebben waarin voldoende emotioneel en fysiek beschikbare opvoeder(s) zijn</li></ul>',
    ), {}),
    ('medische_problemen_mbt_traplopen', forms.BooleanField(
        label=_('Zijn er medische problemen met betrekking tot traplopen?'),
        required=False,
        help_text='',
    ), {}),
     ('medische_problemen_mbt_traplopen_check', forms.IntegerField(
        label=_('Zijn er medische problemen met betrekking tot traplopen?'),
        widget=RadioSelect(
            choices=DEFAULT_NO_OR_YES,
        ),
        required=False,
        help_text='',
    ), {}),
    ('medische_problemen_wooneisen', forms.CharField(
        label=_('Zo ja, benedenwoning of woning met lift? Anders?'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('medische_problemen_bewijslast', forms.FileField(
        label=_('Voeg medische gegevens toe met betrekking tot problematiek'),
        widget=ClearableFileInput(),
        required=False,
    ), {}),
    ('uitsluiting_stadsdeel_argumentatie', forms.CharField(
        label=_('Uitsluiting stadsdeel, argumentatie'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('organisatie', forms.CharField(
        label=_('Organisatie *'),
        required=False,
    ), {'step_required': True}),
    ('persoonlijk_begeleider', forms.CharField(
        label=_('Persoonlijk begeleider *'),
        required=False,
    ), {'step_required': True}),
    ('start_zelfstandig_wonen', forms.CharField(
        label=_('Start zelfstandig wonen (intermediair) *'),
        required=False,
    ), {'step_required': True}),
    ('datum_voordracht', forms.DateField(
        label=_('Datum voordracht *'),
        required=False,
    ), {'step_required': True}),
    ('woningcorporatie_akkoord_met_omklap', forms.IntegerField(
        label=_('Woningcorporatie akkoord met omklap *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('datum_evaluatie_moment', forms.DateField(
        label=_('Datum evaluatie moment *'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_akkoord', forms.IntegerField(
        label=_('Akkoord *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment *'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_akkoord', forms.IntegerField(
        label=_('Akkoord *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment *'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_akkoord', forms.IntegerField(
        label=_('Akkoord *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment *'),
         widget=forms.TextInput(
             attrs={
                 'placeholder': 'dd-mm-jjjj',
             }
         ),
         localize=True,
         required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_akkoord', forms.IntegerField(
        label=_('Akkoord *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment *'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_kinderen_gezonde_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('urgentiecriteria_kinderen_gezonde_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
     ('urgentiecriteria_kinderen_gezonde_akkoord', forms.IntegerField(
        label=_('Akkoord'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
     ), {}),
     ('urgentiecriteria_kinderen_gezonde_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
     ), {}),
     ('omklap_client_openstaande_vragen', forms.CharField(
        label=_('Voor deze cliënt staan de volgende vragen nog open'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
     ), {}),
     ('omklap_client_volgende_stappen_gezet', forms.CharField(
        label=_('Hiervoor worden de volgende stappen gezet (zowel formeel als informeel)'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
     ), {}),
     ('omklap_beoordeeld_door', forms.CharField(
        label=_('Dit is beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
             required = False,
    ), {}),
    ('omklap_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {}),
    ('omklap_toelichting', forms.CharField(
        label=_('Toelichting'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        help_text='Bijvoorbeeld: doelen niet behaald maar geen risico voor zelfstandig wonen',
        required=False,
    ), {}),
    ('omklap_akkoord_derde', forms.IntegerField(
        label=_('Akkoord *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
     ), {'step_required': True}),
    ('omklap_akkoord_derde_toelichting', forms.CharField(
        label=_('Toelichting'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('omklap_akkoord_derde_naam', forms.CharField(
        label=_('Naam / afdeling *'),
        required=False,
    ), {'step_required': True}),
    ('omklap_akkoord_derde_datum', forms.DateField(
        label=_('Datum akkoord *'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {'step_required': True}),
    ('zorginstelling_contactpersoon', forms.CharField(
        label=_('Naam *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False
    ), {'step_required': True}),
    ('zorginstelling_telefoon', forms.CharField(
        label=_('Telefoonnummer *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False
    ), {'step_required': True}),
    ('zorginstelling_emailadres', forms.EmailField(
        label=_('E-mailadres *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('zorginstelling_naam', forms.CharField(
        label=_('Naam zorginstelling *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False
    ), {'step_required': True}),
    ('woningcorporatie_contactpersoon', forms.CharField(
        label=_('Naam *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False
    ), {'step_required': True}),
    ('woningcorporatie_telefoon', forms.CharField(
        label=_('Telefoonnummer *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False
    ), {'step_required': True}),
    ('woningcorporatie_emailadres', forms.EmailField(
        label=_('E-mailadres *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woningcorporatie_naam', forms.CharField(
        label=_('Naam woningcorparatie *'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False
    ), {'step_required': True}),
    ('woningcorporatie_start_intermediaire_verhuur', forms.DateField(
        label=_('Startdatum intermediaire verhuur *'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {'step_required': True}),
    ('woningcorporatie_datum_kennismakingsgesprek', forms.DateField(
        label=_('Datum kennismakingsgesprek *'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {'step_required': True}),
    ('woningcorporatie_datum_woonevaluatiegesprek', forms.DateField(
        label=_('Datum woonevaluatiegesprek *'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {'step_required': True}),
    ('woonevaluatie_ervaring_wonen', forms.CharField(
        label=_('Hoe ervaar je het wonen? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_goed_minder_goed', forms.CharField(
        label=_('Wat gaat goed, wat gaat minder goed? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_omschrijving_woning', forms.CharField(
        label=_('Hoe ziet de woning er uit? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_omschrijving_balkon_tuin', forms.CharField(
        label=_('Hoe ziet het balkon en/of de tuin er uit? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_omschrijving_portiek', forms.CharField(
        label=_('Hoe ziet het portiek er uit? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_contact_met_buren', forms.IntegerField(
        label=_('Heb je contact met buren? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_contact_met_buren_verloop', forms.CharField(
        label=_('Zo ja, hoe verloopt dat?'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('woonevaluatie_contact_met_buren_gewenst', forms.CharField(
        label=_('Zo nee, wil je wel contact? En heb je daar ondersteuning bij nodig?'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('woonevaluatie_overlast_buren', forms.IntegerField(
        label=_('Ervaar je weleens overlast? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_overlast_buren_gemeld', forms.IntegerField(
        label=_('Heb je dit gemeld bij de corporatie? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {}),
    ('woonevaluatie_overlast_omwonenden_gemeld', forms.IntegerField(
        label=_('Is er overlast van omwonenden gemeld? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_overlast_omwonenden_oplossing', forms.CharField(
        label=_('Hoe is daarmee omgegaan? Is het opgelost?'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('woonevaluatie_netwerk_aanwezig', forms.IntegerField(
        label=_('Heb je een netwerk in de buurt? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_netwerk_hoe_gaat_dat', forms.CharField(
        label=_('Zo ja, hoe gaat dat? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_netwerk_behoefte', forms.IntegerField(
        label=_('Zo nee, heb je hier behoefte aan? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_netwerk_behoefte_meer_contacten', forms.CharField(
        label=_('Heb je behoefte aan meer of andere contacten in de buurt? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_huur_betalen_op_tijd', forms.IntegerField(
        label=_('Heb je de huur elke maand op tijd betaald aan de zorgaanbieder? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_huur_betalen_regeling', forms.CharField(
        label=_('Is er een regeling getroffen en/of extra ondersteuning geregeld? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('aanvraag_omklap_actief', forms.IntegerField(
        label=_('Is er sprake van voordracht voor omklap? *'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('aanvraag_omklap_alle_doelen_behaald', forms.CharField(
        label=_('Zijn alle doelen behaald? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('aanvraag_omklap_steunstructuren', forms.CharField(
        label=_('Op welke steunstructuur / structuren kun je een beroep doen na het moment van omklappen? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_moment_volgend_gesprek', forms.CharField(
        label=_('Wat is een goed moment voor het volgende gesprek? *'),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_bijzonderheden_wonen', forms.CharField(
        label=_('Zijn er bijzonderheden rond het wonen? *'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_bewoner', forms.BooleanField(
        label=_('Akkoord bewoner *'),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_bewoner_naam', forms.CharField(
        label=_('Naam *'),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_bewoner_datum', forms.DateField(
        label=_('Datum *'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_zorgaanbieder', forms.BooleanField(
        label=_('Akkoord zorgaanbieder *'),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_zorgaanbieder_naam', forms.CharField(
        label=_('Naam *'),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_zorgaanbieder_datum', forms.DateField(
        label=_('Datum *'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_woningcorporatie', forms.BooleanField(
        label=_('Akkoord woningcorporatie *'),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_woningcorporatie_naam', forms.CharField(
        label=_('Naam *'),
        required=False,
    ), {'step_required': True}),
    ('woonevaluatie_akkoord_woningcorporatie_datum', forms.DateField(
        label=_('Datum *'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {'step_required': True}),
    

    # ('document_list', forms.ModelMultipleChoiceField(
    #     label=_('Documenten lijst'),
    #     # queryset=Document.objects.all(),
    #     required=False,
    # ), {}),
)

FIELDS_DICT = dict((f[0], f[1]) for f in FIELDS)
FIELDS_REQUIRED_DICT = dict((f[0], f[2].get('step_required', False)) for f in FIELDS)

BASIS_GEGEVENS = [
    {
        'title': '',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'client_first_name',
                    'client_last_name',
                    'geboortedatum',
                    'emailadres',
                ],
            },
        ]
    },
]

URGENTIE_AANVRAAG = [
    {
        'title': 'Centrale toegang',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'client_first_name',
                    'client_last_name',
                    'geboortedatum',
                    'emailadres',
                    'centrale_toegang_naam',
                ],
            },
            {
                'title': 'Woningnet',
                'description': '',
                'fields': [
                    'woningnet_nummer',
                    'woningnet_geldigheid',
                ],
            },
            {
                'title': 'Jonger dan 27 jaar?',
                'description': '',
                'fields': [
                    'jonger_dan_26',
                    'jonger_dan_26_plaatsing_project',
                    'jonger_dan_26_motivatie_contract_onbepaalde',
                ],
            },
            {
                'title': 'Gezinssamenstelling',
                'description': '',
                'fields': [
                    'partner_check',
                    'partner_naam',
                    'partner_geboortedatum',
                    'partner_gehuwd',
                    'partner_echtscheiding_rond',
                    'partner_woonsituatie',
                    'kinderen_check',
                    'kinderen',
                ],
            },

        ]
    },
    {
        'title': 'Aanvraag',
        'description': '',
        'section_list': [
            {
                'title': 'Toegang',
                'description': '',
                'fields': [
                    'trajecthouder_naam',
                    'aanvraag_datum',
                    'omslagwoning_zorgaanbieder',
                ],
            },
            {
                'title': 'Urgentiecriteria in de huisvestingsverordening',
                'description': '',
                'fields': [
                    'urgentiecriteria_zinvolle_dagbesteding',
                    'urgentiecriteria_functioneert_sociaal_stabiel',
                    'urgentiecriteria_functioneert_psychisch_stabiel',
                    'urgentiecriteria_is_financieel_stabiel',
                ],
            },
            {
                'title': 'Indien er kinderen gebruik maken van de opvang',
                'id': 'section_kinderen_opvang',
                'description': 'NB: Voor de toewijzing van een woning is de juiste samenstelling van het huishouden in WoningNet relevant. let hierop bij kinderen!',
                'fields': [
                    'urgentiecriteria_kinderen_gezonde_omgeving',
                ],
            },
            {
                'title': 'Toelichting Wooneisen',
                'description': '',
                'fields': [
                    'medische_problemen_mbt_traplopen_check',
                    'medische_problemen_wooneisen',
                    'uitsluiting_stadsdeel_argumentatie',
                ],
            },

        ]
    },
    {
        'title': 'Bijlagen',
        'description': "<strong>Nodige bijlagen bij aanvraag Urgentie onder voorwaarden</strong><ul><li>kopie ID</li><li>meest recente IB60/ IBRI (jaaropgave van de belastingdienst)</li><li>meest recente loonstrook</li><li>meest recente plaatsingsbesluit veldtafel, WMO beschikking of SPIC</li></ul><p><strong>Indien partner in zelfde woning zal wonen:</strong></p><ul><li>kopie ID partner (geen rijbewijs)</li><li>meest recente IB60/ IBRI (jaaropgave van de belastingdienst) partner</li><li>meest recente loonstrook partner</li></ul><p><strong>Let op: </strong>Medische gegevens mogen niet bij de aanvraag meegestuurd worden</p>",
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'document_list',
                ],
            },
        ]
    },
]

OMKLAP_AANVRAAG = [
    {
        'title': 'Woningnet',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'client_first_name',
                    'client_last_name',
                    'geboortedatum',
                    'emailadres',
                    'woningnet_nummer',
                    'woningnet_geldigheid',
                ],
            },
        ]
    },
    {
        'title': 'Organisatie en voordracht',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'organisatie',
                    'persoonlijk_begeleider',
                    'start_zelfstandig_wonen',
                    'datum_voordracht',
                ],
            },
        ]
    },
    {
        'title': 'Woonevaluatie gesprek',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'woningcorporatie_akkoord_met_omklap',
                    'datum_evaluatie_moment',
                ],
            },
        ]
    },
    {
        'title': 'Jonger dan 27 jaar?',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'jonger_dan_26',
                    'jonger_dan_26_plaatsing_project',
                    'jonger_dan_26_motivatie_contract_onbepaalde',
                ],
            },
        ]
    },
    {
        'title': 'Urgentiecriteria in de huisvestingsverordening',
        'description': '',
        'section_list': [
            {
                'title': 'Zinvolle dagbesteding',
                'description': '',
                'fields': [
                    'urgentiecriteria_zinvolle_dagbesteding',
                    'urgentiecriteria_zinvolle_dagbesteding_behaald_omdat',
                    'urgentiecriteria_zinvolle_dagbesteding_beoordeeld_door',
                    'urgentiecriteria_zinvolle_dagbesteding_akkoord',
                    'urgentiecriteria_zinvolle_dagbesteding_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'Sociaal',
                'description': '',
                'fields': [
                    'urgentiecriteria_functioneert_sociaal_stabiel',
                    'urgentiecriteria_functioneert_sociaal_behaald_omdat',
                    'urgentiecriteria_functioneert_sociaal_beoordeeld_door',
                    'urgentiecriteria_functioneert_sociaal_akkoord',
                    'urgentiecriteria_functioneert_sociaal_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'Psychisch',
                'description': '',
                'fields': [
                    'urgentiecriteria_functioneert_psychisch_stabiel',
                    'urgentiecriteria_functioneert_psychisch_behaald_omdat',
                    'urgentiecriteria_functioneert_psychisch_beoordeeld_door',
                    'urgentiecriteria_functioneert_psychisch_akkoord',
                    'urgentiecriteria_functioneert_psychisch_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'Financieel',
                'description': '',
                'fields': [
                    'urgentiecriteria_is_financieel_stabiel',
                    'urgentiecriteria_is_financieel_stabiel_behaald_omdat',
                    'urgentiecriteria_is_financieel_stabiel_beoordeeld_door',
                    'urgentiecriteria_is_financieel_stabiel_akkoord',
                    'urgentiecriteria_is_financieel_stabiel_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'En, indien er kinderen gebruik maken van de opvang',
                'description': '',
                'fields': [
                    'urgentiecriteria_kinderen_gezonde_omgeving',
                    'urgentiecriteria_kinderen_gezonde_behaald_omdat',
                    'urgentiecriteria_kinderen_gezonde_beoordeeld_door',
                    'urgentiecriteria_kinderen_gezonde_akkoord',
                    'urgentiecriteria_kinderen_gezonde_datum_evaluatiemoment',
                ],
            },
        ]
    },
    {
        'title': 'Afspraken na de omklap',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'omklap_client_openstaande_vragen',
                    'omklap_client_volgende_stappen_gezet',
                    'omklap_beoordeeld_door',
                    'omklap_datum_evaluatiemoment',
                ],
            }
        ],
    },
    {
        'title': 'Toelichting',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'omklap_toelichting',
                ],
            }
        ],
    },
    {
        'title': 'Akkoord objectieve derde',
        'description': "",
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'omklap_akkoord_derde',
                    'omklap_akkoord_derde_toelichting',
                    'omklap_akkoord_derde_naam',
                    'omklap_akkoord_derde_datum'
                ],
            },
        ]
    },
    {
        'title': 'Bijlagen',
        'description': "<strong>Nodige bijlagen bij aanvraag Voordracht omklap</strong><ul><li>meest recente IB60/ IBRI (jaaropgave van de belastingdienst)</li><li>meest recente loonstrook</li><li>meest recente plaatsingsbesluit veldtafel, WMO beschikking of SPIC</li></ul>",
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'document_list',
                ],
            },
        ]
    },
]

EVALUATIE_WONEN = [
    {
        'title': 'Contactpersoon zorgaanbieder',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'zorginstelling_contactpersoon',
                    'zorginstelling_telefoon',
                    'zorginstelling_emailadres',
                    'zorginstelling_naam',
                ],
            },
        ]
    },
    {
        'title': 'Contactpersoon woningcorporatie',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'woningcorporatie_contactpersoon',
                    'woningcorporatie_telefoon',
                    'woningcorporatie_emailadres',
                    'woningcorporatie_naam',
                ],
            },{
                'title': '',
                'description': '',
                'fields': [
                    'woningcorporatie_start_intermediaire_verhuur',
                    'woningcorporatie_datum_kennismakingsgesprek',
                    'woningcorporatie_datum_woonevaluatiegesprek',
                ],
            },
        ]
    },
    {
        'title': 'Landen in de woning',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'woonevaluatie_ervaring_wonen',
                    'woonevaluatie_goed_minder_goed',
                ],
            },
        ]
    },
    {
        'title': 'Woning',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'woonevaluatie_omschrijving_woning',
                    'woonevaluatie_omschrijving_balkon_tuin',
                    'woonevaluatie_omschrijving_portiek',
                ],
            },
        ]
    },
    {
        'title': 'Omgeving',
        'description': '',
        'section_list': [
            {
                'title': 'Contact met buren',
                'description': '',
                'fields': [
                    'woonevaluatie_contact_met_buren',
                    'woonevaluatie_contact_met_buren_verloop',
                    'woonevaluatie_contact_met_buren_gewenst',
                ],
            },
            {
                'title': 'Overlast en de buren',
                'description': '',
                'fields': [
                    'woonevaluatie_overlast_buren',
                    'woonevaluatie_overlast_buren_gemeld',
                    'woonevaluatie_overlast_omwonenden_gemeld',
                    'woonevaluatie_overlast_omwonenden_oplossing',
                ],
            },
            {
                'title': 'Netwerk in de buurt',
                'description': '',
                'fields': [
                    'woonevaluatie_netwerk_aanwezig',
                    'woonevaluatie_netwerk_hoe_gaat_dat',
                    'woonevaluatie_netwerk_behoefte',
                    'woonevaluatie_netwerk_behoefte_meer_contacten',
                ],
            },
            
        ]
    },
    {
        'title': 'Huurbetaling',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'woonevaluatie_huur_betalen_op_tijd',
                    'woonevaluatie_huur_betalen_regeling',
                ],
            },
        ]
    },
    {
        'title': 'Stand van zaken gepersonaliseerde doelen rond het wonen',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'urgentiecriteria_zinvolle_dagbesteding',
                    'urgentiecriteria_functioneert_sociaal_stabiel',
                    'urgentiecriteria_functioneert_psychisch_stabiel',
                    'urgentiecriteria_is_financieel_stabiel',
                ],
            }
        ]
    },
    {
        'title': 'Is er sprake van voordracht voor omklap?',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'aanvraag_omklap_actief',
                    'aanvraag_omklap_alle_doelen_behaald',
                    'aanvraag_omklap_steunstructuren',
                ],
            }
        ]
    },
    {
        'title': 'Vervolg',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'woonevaluatie_moment_volgend_gesprek',
                    'woonevaluatie_bijzonderheden_wonen',
                ],
            }
        ]
    },
    {
        'title': 'Akkoord',
        'description': '',
        'section_list': [
            {
                'title': 'Bewoner',
                'description': '',
                'fields': [
                    'woonevaluatie_akkoord_bewoner',
                    'woonevaluatie_akkoord_bewoner_naam',
                    'woonevaluatie_akkoord_bewoner_datum'
                ],
            },
            {
                'title': 'Zorgaanbieder',
                'description': '',
                'fields': [
                    'woonevaluatie_akkoord_zorgaanbieder',
                    'woonevaluatie_akkoord_zorgaanbieder_naam',
                    'woonevaluatie_akkoord_zorgaanbieder_datum'
                ],
            },
            {
                'title': 'Woningcorporatie',
                'description': '',
                'fields': [
                    'woonevaluatie_akkoord_woningcorporatie',
                    'woonevaluatie_akkoord_woningcorporatie_naam',
                    'woonevaluatie_akkoord_woningcorporatie_datum'
                ],
            },
        ]
    }
]

FORMS = (
    (
        'basis_gegevens',
        BASIS_GEGEVENS,
        'basis-gegevens',
        'Basisgegevens cliënt',
        'Nieuwe cliënt',
        False,
        False,
        False,
        {'exclude_fields': []},
    ),
    (
        'urgentie_aanvraag',
        URGENTIE_AANVRAAG,
        'aanvraag-omslag-en-urgentie',
        'Aanvraag Urgentie onder voorwaarden',
        'Nieuwe aanvraag Urgentie onder voorwaarden',
        True,
        True,
        True,
        FEDERATION_TYPE_ADW,
        {'exclude_fields': [
            'client_first_name',
            'client_last_name',
            'geboortedatum',
            'emailadres',
        ], 'rules': {
            'jonger_dan_26': ([3,4], (
                'jonger_dan_26_plaatsing_project',
                'jonger_dan_26_motivatie_contract_onbepaalde',
                )),
            'partner_check': ([1], (
                'partner_naam',
                'partner_geboortedatum',
                'partner_gehuwd',
                'partner_echtscheiding_rond',
                'partner_woonsituatie',
                )),
            'kinderen_check': ([1], (
                'kinderen',
                'section_kinderen_opvang',
                )),
            'medische_problemen_mbt_traplopen_check': ([1], (
                'medische_problemen_wooneisen',
            ))

        }},
    ),
    (
        'omklap_aanvraag',
        OMKLAP_AANVRAAG,
        'aanvraag-omklap',
        'Aanvraag Voordracht omklap',
        'Nieuwe aanvraag Voordracht omklap',
        True,
        True,
        True,
        FEDERATION_TYPE_ADW,
        {'exclude_fields': [
            'client_first_name',
            'client_last_name',
            'geboortedatum',
            'emailadres',
        ],'rules': {
            'jonger_dan_26': ([3,4], (
                'jonger_dan_26_plaatsing_project',
                'jonger_dan_26_motivatie_contract_onbepaalde',
                )),
            'omklap_akkoord_derde': ([2], (
                ['omklap_akkoord_derde_toelichting']
                )),
        }, 'addres_required': True},
    ),
    (
        'evaluatie_wonen',
        EVALUATIE_WONEN,
        'evaluatie-wonen',
        'Evaluatie wonen',
        'Nieuwe evaluatie wonen',
        True,
        True,
        True,
        {'exclude_fields': [
            'client_first_name',
            'client_last_name',
            'geboortedatum',
            'emailadres',
        ]
        ,'rules': {
        
            'woonevaluatie_overlast_buren': ([1], (
                ['woonevaluatie_overlast_buren_gemeld']
            )),
            'woonevaluatie_overlast_omwonenden_gemeld': ([1], (
                ['woonevaluatie_overlast_omwonenden_oplossing']
            )),
            'woonevaluatie_huur_betalen_op_tijd': ([2], (
                ['woonevaluatie_huur_betalen_regeling']
            )),

            'aanvraag_omklap_actief': ([1], (
                ['aanvraag_omklap_alle_doelen_behaald',
                'aanvraag_omklap_steunstructuren']
            )),
            
        }},
    ),
    (
        'evaluatie_wonen',
        EVALUATIE_WONEN,
        'evaluatie-wonen',
        'Evaluatie wonen',
        'Nieuwe evaluatie wonen',
        True,
        True,
        True,
        {'exclude_fields': [
            'client_first_name',
            'client_last_name',
            'geboortedatum',
            'emailadres',
        ]},
    ),
)

FORMS_PROCESSTAP = [
    'aanvraag-omslag-en-urgentie',
    'evaluatie-wonen',
    'aanvraag-omklap',
]


def map_form_keys(f):
    return {
        'key': f[0],
        'sections': f[1],
        'slug': f[2],
        'title': f[3],
        'title_new': f[4],
        'inpage_navigation': f[5],
        'share': f[6],
        'enable_ajax': f[7],
        'federation_type': f[8],
        'options': f[9] if len(f) > 9 else {},
    }


FORMS_BY_KEY = dict((s[0], map_form_keys(s)) for s in FORMS)
FORMS_BY_SLUG = dict((s[2], map_form_keys(s)) for s in FORMS)
FORMS_CHOICES = [[s[2], s[3]] for s in FORMS]
FORMS_PROCESSTAP_CHOICES = [[s[2], s[3]] for s in FORMS if s[2] in FORMS_PROCESSTAP]

FORM_TITLE_BY_SLUG = dict((s[2], s[3]) for s in FORMS)

FORMS_SLUG_BY_FEDERATION_TYPE = dict((ft[0], [f[2] for f in FORMS if f[8] == ft[0]])for ft in FEDERATION_TYPE_CHOICES)
