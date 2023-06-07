from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "yeager_ai.user_profile"
    
    def ready(self):
        import yeager_ai.user_profile.signals