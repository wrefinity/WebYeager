from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField, DateTimeField, CharField, EmailField, CharField, PositiveIntegerField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

'''
TimeStampedModel: Abstract base classes for meant to be instantiated 
when inherited by other models. 
'''


class TimeStampedModel(models.Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """
    Default custom user model for YeagerAI Web App.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("Users FirstName"), blank=True, max_length=100)
    last_name = CharField(_("Users Last Name"), blank=True, max_length=100)
    email = EmailField(_('email address'), unique=True, blank=True)
    is_admin = BooleanField(_('role type'), default=False)
    karma = PositiveIntegerField(verbose_name="karma", default=0, blank=True)

    def __str__(self):
        return f"{self.email}"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.pk})
