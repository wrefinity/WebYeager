from django.urls import path

from .views import login_redirect

urlpatterns = [
    path("", login_redirect, name="login_redirect")
]
