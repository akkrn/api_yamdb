import re

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True,
                                   validators=[UniqueValidator(
                                       queryset=User.objects.all())]
                                   )
    username = serializers.CharField(max_length=150,validators=[UniqueValidator(
                                       queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("username", "email"),
                message="Такой пользователь уже существует",
            ),
        ]

    def validate_username(self, value):
        if value.lower() == "me" and value != r'^[\w.@+-]+\z':
            raise serializers.ValidationError('Нельзя использовать такое имя!')
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.save()
        return user

class UserMeSerializer(UserSerializer):
    class Meta:
        read_only_fields = ("id", "role",)


class ConfirmationCodeSerializer(TokenObtainSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = (
            "username",
            "confirmation_code",
        )
        model = User

class TestUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)

