from django.urls import reverse_lazy
from django.views.generic import RedirectView


class LoginRedirectView(RedirectView):
    
    def get_redirect_url(self, **kwargs):
        if self.request.user:
            return reverse_lazy('worlds:world_list')
        else:
            return reverse_lazy('account_login')
login_redirect = LoginRedirectView.as_view()