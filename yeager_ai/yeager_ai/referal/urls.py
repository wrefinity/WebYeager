from django.urls import path
from . import views

app_name = "referrals"

urlpatterns = [
    path('', views.ReferralProfileView.as_view(), name='view-referral-profile'),
]
