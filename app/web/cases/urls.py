from .views import *
from django.urls import path
from web.forms.statics import URGENTIE_AANVRAAG, BASIS_GEGEVENS


urlpatterns = [
    path('mijn-clienten/', UserCaseList.as_view(), name='cases_by_profile'),
    # path('nieuw/', CaseCreateView.as_view(), name='add_case'),
    path('<int:pk>', CaseDetailView.as_view(), name='case'),
    path('wijzig/<int:pk>', GenericFormView.as_view(), {
        'title': 'Wijzig cliënt basisgegevens',
        'sections': BASIS_GEGEVENS,
    }, name='update_case'),
    path('verwijder/<int:pk>', CaseDeleteView.as_view(), name='delete_case'),

    # urgentie aanvraag en omslag
    path('<int:pk>/nieuwe-aanvraag-omslag-en-urgentie', GenericFormView.as_view(), {
        'title': 'Nieuwe aanvraag omslag en urgentie',
        'sections': URGENTIE_AANVRAAG
    }, name='nieuwe_aanvraag_omslag_en_urgentie'),
    path('<int:pk>/nieuwe-aanvraag-omslag-en-urgentie/verstuur', SendCaseView.as_view(), {
        'title': 'Nieuwe aanvraag omslag en urgentie',
        'sections': URGENTIE_AANVRAAG
    }, name='nieuwe_aanvraag_omslag_en_urgentie_send'),


    path('nieuw/', GenericCaseCreateFormView.as_view(), {
        'title': 'Nieuwe cliënt',
        'sections': BASIS_GEGEVENS,
    }, name='add_case'),
]
