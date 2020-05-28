from rest_framework import routers
from web.cases.viewsets import CaseStatusUpdateViewSet

router = routers.DefaultRouter()
router.register(r'casestatus', CaseStatusUpdateViewSet)