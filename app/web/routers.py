from rest_framework import routers
from web.cases.viewsets import CaseStatusUpdateViewSet, CaseUpdateDossierNrViewSet

router = routers.DefaultRouter()
router.register(r'casestatus', CaseStatusUpdateViewSet)
router.register(r'case-dossier-nr', CaseUpdateDossierNrViewSet)