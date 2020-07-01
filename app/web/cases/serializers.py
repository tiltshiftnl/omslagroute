from rest_framework import serializers
from .models import CaseStatus, Case
from web.profiles.models import Profile
from web.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user']


class CaseStatusSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="profile.user.username")

    class Meta:
        model = CaseStatus
        fields = '__all__'


class CaseDossierNrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            'wonen_dossier_nr',
        ]