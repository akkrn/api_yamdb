from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.RegexField(
        regex="^[\\w.@+-]+",
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

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
        if value.lower() == "me":
            raise serializers.ValidationError("Нельзя использовать такое имя!")
        return value

    def create(self, validated_data):
        if self.is_valid():
            user, created = User.objects.get_or_create(**validated_data)
            user.save()
        return user


class UserMeSerializer(UserSerializer):
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
        read_only_fields = (
            "id",
            "role",
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = (
            "username",
            "confirmation_code",
        )
        model = User


class SignupSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )
