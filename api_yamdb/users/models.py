from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        USER = "user", _("User")
        MODERATOR = "moderator", _("Moderator")
        ADMIN = "admin", _("Admin")

    email = models.EmailField(blank=False, max_length=264, unique=True)
    role = models.CharField(
        max_length=10,
        blank=True,
        choices=RoleChoice.choices,
        default=RoleChoice.USER,
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
