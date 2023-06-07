from django.db import models
from django.contrib.auth import get_user_model
# from yeager_ai.billing.models import WorldBilling
from yeager_ai.users.models import TimeStampedModel
from django.db.models import CharField, TextField, \
    CharField, ForeignKey, FloatField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.
User = get_user_model()


class Payment(TimeStampedModel):
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = FloatField()
    ref_number = CharField(_("Reference Key"), blank=True, max_length=255)
    customer_email = EmailField(_('customers email address'), blank=True)
    payment_method_types = CharField(
        _("Payment Method"), blank=True, max_length=50)
    payment_intent = CharField(_("Payment intent"), blank=True, max_length=255)
    description = TextField(null=True, blank=True)
    # the field keep track of succesful payments
    has_paid = models.BooleanField(
        default=False, verbose_name='Payment Status')

    def __str__(self):
        return f'{self.user.first_name} payment'

    def get_my_payment(self):
        return Payment.objects.filter(user=self.user)

    @property
    def payment_list(self):
        return self.get_my_payment()

    def get_absolute_url(self):
        return reverse("payment:details", kwargs={"uuid": self.uuid})


# model for invoice
class Invoice(TimeStampedModel):
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = ForeignKey(Payment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.payment.user} invoice'

    def get_absolute_url(self):
        return reverse("invoice_detail", kwargs={"uuid": self.uuid})
