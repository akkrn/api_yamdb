from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    role_choices = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    email = models.EmailField(blank=False, max_length=264, unique=True)
    role = models.CharField(max_length=10, blank=True, choices=role_choices,
                            default="user")
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    objects = CustomUserManager()


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_user"
            )
        ]
