from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("role", "admin")
        return super().create_superuser(
            username, email, password, **extra_fields
        )
