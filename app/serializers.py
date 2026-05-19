from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_admin'] = user.is_admin  

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "id", "username", "email", "is_staff"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and not request.user.is_staff:
            # Hide staff field for non-admins
            self.fields.pop("is_staff")
            self.fields.pop("url")

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=4, allow_blank=False)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Profile
        fields = ["username", "location", "bio", "profile_picture"]

class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        """Ensure password and password2 match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # remove password2
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
        )
        return user
        
        
class LoginSerializer(serializers.Serializer):
    """Serializer pour le login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
)

