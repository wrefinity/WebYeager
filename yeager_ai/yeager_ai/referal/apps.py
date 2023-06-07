from django.apps import AppConfig


class ReferralsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "yeager_ai.referal"

    def ready(self):
        from . import signals
        