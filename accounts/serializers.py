from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from accounts.models import User


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'point')
