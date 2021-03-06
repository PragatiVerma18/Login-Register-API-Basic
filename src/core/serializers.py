from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_user', 'is_org')


class CustomRegisterSerializer(RegisterSerializer):
    is_user = serializers.BooleanField()
    is_org = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_user', 'is_org')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'is_user': self.validated_data.get('is_user', ''),
            'is_org': self.validated_data.get('is_org', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_user = self.cleaned_data.get('is_user')
        user.is_org = self.cleaned_data.get('is_org')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key', 'user', 'user_type')

    def get_user_type(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        is_user = serializer_data.get('is_user')
        is_org = serializer_data.get('is_org')
        return {
            'is_user': is_user,
            'is_org': is_org
        }
