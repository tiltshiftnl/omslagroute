from .views import *
from django.urls import path
from web.forms.statics import URGENTIE_AANVRAAG


urlpatterns = [
    path('mijn-clienten/', UserCaseList.as_view(), name='cases_by_profile'),
    path('nieuw/', CaseCreateView.as_view(), name='add_case'),
    path('<int:pk>', CaseDetailView.as_view(), name='case'),
    path('wijzig/<int:pk>', CaseUpdateView.as_view(), name='update_case'),
    path('verwijder/<int:pk>', CaseDeleteView.as_view(), name='delete_case'),
    path('<int:pk>/nieuwe-aanvraag-omslag-en-urgentie', GenericFormView.as_view(), {
        'title': 'Aanvraag urgentie',
        'sections': URGENTIE_AANVRAAG
    }, name='nieuwe_aanvraag_omslag_en_urgentie'),
]
