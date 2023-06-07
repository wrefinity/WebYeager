from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
# from .models import UserProfile
from django import forms

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': ' form-control bg-transparent'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': ' form-control bg-transparent'}))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email Address', 'class': ' form-control bg-transparent'}))

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'enter password', 'class': 'form-control bg-transparent'})
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'This email address already exists. Please use a different email.')
        return cleaned_data
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    

    def save(self, request):
        try:
            user = super(UserSignupForm, self).save(request)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            return user
        except IntegrityError:
            self.add_error('email', 'This username already exists. Please choose a different username.')
            


class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': ' form-control bg-transparent'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder': 'password', 'class': ' form-control bg-transparent'})


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
