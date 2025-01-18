import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    is_unknown_user = models.BooleanField(default=False)
    email = models.EmailField(_("email address"), blank=True, unique=True)

    @property
    def is_admin(self):
        return self.is_staff

    @property
    def is_expert(self):
        return self.groups.filter(name="Experts").exists()


class UserResetKey(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="reset_key"
    )
    reset_key = models.UUIDField(default=uuid.uuid4, null=True)
    reset_key_datetime = models.DateTimeField(null=True, blank=True)
