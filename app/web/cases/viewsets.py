from rest_framework import viewsets
from .models import Case
from .serializers import CaseSerializer
from django.contrib.auth.mixins import UserPassesTestMixin
from web.users.statics import BEGELEIDER
from web.users.auth import auth_test


class CaseViewSet(UserPassesTestMixin, viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return self.request.user.profile.cases.all()
