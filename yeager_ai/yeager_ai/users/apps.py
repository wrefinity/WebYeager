from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "yeager_ai.users"
    verbose_name = _("Users")

    def ready(self):
        import yeager_ai.users.signals  # noqa: F401