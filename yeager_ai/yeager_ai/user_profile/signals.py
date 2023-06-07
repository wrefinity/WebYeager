from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CreditModel
User = get_user_model()

'''
create a credit account for new user
'''
@receiver(post_save, sender=User)
def create_credit_model(sender, instance, created, **kwargs):
    if created:
        CreditModel.objects.create(user=instance)