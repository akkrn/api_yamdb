from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = models.TextChoices("role", "user moderator admin")
    email = models.EmailField(blank=False, max_length=264, unique=True)
    role = models.CharField(
        max_length=10, blank=True, choices=ROLE_CHOICES.choices, default="user"
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_user"
            )
        ]

    def __str__(self):
        return self.username
