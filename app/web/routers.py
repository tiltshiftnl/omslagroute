from rest_framework import routers
from web.cases.viewsets import CaseViewSet

router = routers.DefaultRouter()
router.register(r'case', CaseViewSet)
