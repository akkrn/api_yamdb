from rest_framework.validators import UniqueTogetherValidator

from .models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.SlugRelatedField(required=True,
                                            slug_field="username")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio",
                  "role")
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("username", "email"),
                message="Такой пользователь уже существует",
            )
        ]

    def create(self, validated_data):
        user = User.objects.get_or_create(
            validated_data['username'],
            validated_data['email'],
        )
        return user


