from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserReferral

# Create your views here.


class ReferralProfileView(LoginRequiredMixin, TemplateView):
    template_name = "pages/Referrals/referral.html"
    context_object_name = "referal_list"

    def get_context_data(self, **kwargs):
        kwargs = super(ReferralProfileView, self).get_context_data(**kwargs)
        # print("User is", self.request.user, self.request.user.email)
        kwargs["referralProfile"] = get_object_or_404(UserReferral, user=self.request.user)
        return kwargs
