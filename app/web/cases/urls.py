from .views import *
from django.urls import path
from web.timeline.models import Moment


urlpatterns = [
    path('mijn-clienten/', UserCaseList.as_view(), name='cases_by_profile'),
    path('nieuw/', CaseCreateView.as_view(), name='add_case'),
    path('wijzig/<int:pk>', CaseUpdateView.as_view(), name='update_case'),
    path('verwijder/<int:pk>', CaseDeleteView.as_view(), name='delete_case'),
]
