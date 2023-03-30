from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role_choices = [
        ('U', 'user'),
        ('M', 'moderator'),
        ('A', 'admin'),
    ]
    email = models.EmailField(blank=False, max_length=264, unique=True)
    role = models.CharField(max_length=1, blank=True, choices=role_choices,
                            default="user")
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_user"
            )
        ]
