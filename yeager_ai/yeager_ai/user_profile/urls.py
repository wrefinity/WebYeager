from django.urls import path

from yeager_ai.user_profile.views import user_profile_view, account_overview
app_name = "users_profile"
urlpatterns = [
    path("", view=user_profile_view, name="users_profile"),
    path("account_overview", view=account_overview, name="account_overview"),
]
