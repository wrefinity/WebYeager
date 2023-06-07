from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import decimal

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=255, blank=True, null=True)
    phone = models.TextField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatar/', default='default.png', blank=True, null=False)

    def __str__(self):
        return f'{self.user.first_name} profile'

    def get_success_url(self):
        return reverse('users_profile:users_profile', kwargs={'pk': self.object.pk})


'''
Users credit modules
'''


class CreditModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal('0.00'), editable=False)


    def __str__(self):
        return f'{self.user.first_name} credits = {self.total_credit}'

    # for adding credit upon user subcriptions
    def add_credit(self, amount):
        # amount in usd
        # 1 usd = 50.0 credit
        try:
            default_credit = decimal.Decimal('50.0')
            amount_decimal = decimal.Decimal(str(amount))
            new_credit = amount_decimal * default_credit
            self.total_credit += new_credit
            self.save()
        except Exception as e:
            print("An error occurred:", str(e))

    def debit_credit(self):
        debit_tokens = 1  # token to be debited
        if self.total_credit >= debit_tokens:
            self.total_credit -= debit_tokens
            self.save()
            return True  # credit deducted
        return False  # insufficient balance
