import uuid
from django.db import models
from yeager_ai.users.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db.models import BooleanField, CharField, \
    TextField, CharField, ForeignKey
from django.urls import reverse
from enum import Enum
from django.utils.translation import gettext_lazy as _


# Create your models here.
User = get_user_model()


class PlatformEnum(Enum):
    PLATFORM_A = "OpenAI"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ApiKey(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    key = CharField(max_length=100, unique=True)
    platform = models.CharField(
        max_length=50,
        choices=PlatformEnum.choices(),
        default=PlatformEnum.PLATFORM_A.value,
    )
    description = TextField()
    is_active = BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform} - {self.key}"

    # get api keys created by current user
    def get_my_keys(self):
        return ApiKey.objects.filter(user=self.user)

    def get_absolute_url(self):
        return reverse("api_keys:api_key_detail", kwargs={"uuid": self.uuid})
