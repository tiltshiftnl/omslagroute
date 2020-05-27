from rest_framework import viewsets, mixins
from .models import CaseStatus
from .serializers import CaseStatusSerializer
from django.contrib.auth.mixins import UserPassesTestMixin
from web.users.statics import BEGELEIDER
from web.users.auth import auth_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


class CaseStatusUpdateViewSet(UserPassesTestMixin, mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer

    def test_func(self):
        return auth_test(self.request.user, BEGELEIDER) and hasattr(self.request.user, 'profile')

    def get_queryset(self):
        return CaseStatus.objects.all()

    def create(self, request, *args, **kwargs):
        print(request)
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        return super().create(request=request, *args, **kwargs)


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)