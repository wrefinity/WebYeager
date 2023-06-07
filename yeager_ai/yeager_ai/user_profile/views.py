from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm
from .models import UserProfile, CreditModel
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, UpdateView, View


# Create your views here.
class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    login_url = "/accounts/login"
    template_name = "pages/Account/account_settings.html"
    success_url = reverse_lazy('users_profile:users_profile')

    def get_object(self):
        return self.request.user.userprofile

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


user_profile_view = UserProfileView.as_view()


class AccountOverView(LoginRequiredMixin, TemplateView):
    login_url = "/accounts/login"
    template_name = "pages/Account/account_overview.html"


account_overview = AccountOverView.as_view()


''' 
a view to test debit transaction
'''    
class DebitView(LoginRequiredMixin, View):
    template_name = 'debit.html'
    success_url = reverse_lazy('success')
    login_url = "/accounts/login"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        amount = request.POST.get('amount')
        user_account = CreditModel.objects.get(user=request.user)
        if user_account.debit_credit(float(amount)):
            return redirect(self.success_url)
        else:
            error_message = 'Insufficient funds'
            return render(request, self.template_name, {'error_message': error_message})