from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from allauth.account.signals import user_signed_up
from django.views.generic import DetailView, TemplateView, View, ListView, RedirectView, UpdateView,\
    UpdateView

User = get_user_model()


class UserOverView(TemplateView):
    template_name = "pages/User/user_detail.html"
user_over_view = UserOverView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "pk"
    slug_url_kwarg = "pk"

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserListView(ListView, LoginRequiredMixin):
    model = User
    template_name = "pages/User/users.html"
    context_object_name = 'user_list'


user_list_view = UserListView.as_view()


class UserLogoutView(View):

    def get(self, request,  *args, **kwargs):
        auth.logout(request)
        return redirect("account_login")


user_logout_view = UserLogoutView.as_view()
