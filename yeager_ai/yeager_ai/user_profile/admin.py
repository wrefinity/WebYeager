from django.contrib import admin
from yeager_ai.user_profile.models import UserProfile, CreditModel


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CreditModel)