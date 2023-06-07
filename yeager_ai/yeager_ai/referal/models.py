from django.db import models
from django.contrib.auth import get_user_model
import math

# Create your models here.
User = get_user_model()


class UserReferral(models.Model):
    user = models.OneToOneField(
        User, related_name="referral_profile", on_delete=models.CASCADE)
    invited_by = models.ForeignKey(
        User, related_name="referred_by", on_delete=models.SET_NULL, null=True)
    invite_code = models.CharField(max_length=10, unique=True)
    earnings = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}  {self.user.last_name} Referral Profile"
    

    def get_referred_by_me(self):
        return UserReferral.objects.filter(invited_by=self.user)
    # return list of people referred by me
    # invited_by(user)

    @property
    def referral_list(self):
        return self.get_referred_by_me()

    @staticmethod
    def get_profile(user):
        return User.objects.get(user=user)

    def get_earnings(self):
        return ReferralEarning.objects.filter(profile=self)

    def invite_count(self):
        return self.get_referred_by_me().count()


class ReferralEarning(models.Model):
    profile = models.ForeignKey(UserReferral, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    earned_points = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.00, editable=False)
    source = models.ForeignKey(
        User, related_name="earning_source", on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    # ReferralEarning.add_earning(profile=Sunday, source=Andrew, amount=50)

    @classmethod
    def add_earning(cls, profile: UserReferral, source: User, amount=0.00):
        # 1 usd = 2 points
        earnings = 100  # points
        if amount:
            # if amount is set, do the math
            if amount >= 1:
                # convert usd to points
                earnings = math.ceil(amount) * 2

        cls.objects.create(
            profile=profile,
            source=source,
            amount=amount,
            earned_points=earnings)
        profile.earnings += earnings
        profile.save()