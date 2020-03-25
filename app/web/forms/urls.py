from .views import *
from .forms import *
from django.urls import path
from .statics import URGENTIE_AANVRAAG, AANVRAAG_VERLENGING_TRACJECTWIJZIGING_MOBW


urlpatterns = [
    path('', FormListView.as_view(), name='form_list'),

    path('aanvraag-urgentie',  GenericFormView.as_view(), {
        'title': 'Aanvraag urgentie',
        'sections': URGENTIE_AANVRAAG,
    }, name='aanvraag_urgentie'),

    path('aanvraag-verlenging-trajectwijziging-mobw', GenericFormView.as_view(), {
        'title': 'Aanvraag verlenging trajectwijziging MOBW',
        'sections': AANVRAAG_VERLENGING_TRACJECTWIJZIGING_MOBW,
    }, name='aanvraag_verlenging_trajectwijziging_mobw'),
]
