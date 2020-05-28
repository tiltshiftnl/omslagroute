from rest_framework import viewsets, mixins
from .models import CaseStatus
from .serializers import CaseStatusSerializer
from django.contrib.auth.mixins import UserPassesTestMixin
from web.users.statics import BEGELEIDER, WONEN
from web.users.auth import auth_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from django.contrib.auth.models import User


class CaseStatusUpdateViewSet(UserPassesTestMixin, viewsets.ModelViewSet):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer

    def test_func(self):
        return auth_test(self.request.user, [BEGELEIDER, WONEN]) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return CaseStatus.objects.all().order_by('-created')

    def create(self, request, *args, **kwargs):
        data = {'profile': request.user.profile.id}
        data.update(request.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)