# Signals
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth import get_user_model
from .models  import UserReferral, ReferralEarning


User = get_user_model()


def gen_invite_code():
	return get_random_string(length=8)

@receiver(social_account_added)
@receiver(user_signed_up)
def update_referral_profile(sender, **kwargs):
	print("kwargs is", kwargs)
	request = kwargs.pop("request", None)
	user = kwargs.pop("user", None)
	sociallogin = kwargs.pop("sociallogin", None)
	# kwargs is {'signal': <django.dispatch.dispatcher.Signal object at 0x11115e400>, 'request': <WSGIRequest: GET '/accounts/github/login/callback/?code=c399db0774e7f37d47b9&state=7xXYrEvuakZG'>, 'user': <User: damilola>, 'sociallogin': <allauth.socialaccount.models.SocialLogin object at 0x11354a2e0>}

	user = user
	 # or social
	# if sociallogin:
	# 	user = sociallogin.account.user
	if request and user:
		invite_code = request.session.pop("invite_code", None)
		print("invite_code in signal is", invite_code)
		ref = UserReferral.objects.filter(invite_code = invite_code)
		referral = None
		print("\n"*12)
		print("Got to 39:")
		if ref.exists():
			referral = ref.first()
			print("referral is", referral)
			refProfile = UserReferral.objects.get(user = user)
			refProfile.invited_by = referral.user
			refProfile.save()
			ReferralEarning.add_earning(profile=referral, source=user)
			print("Referral Profile saved")


@receiver(post_save, sender=User)
def create_referral_profile(sender, instance, created, *args, **kwargs):
	if created and not UserReferral.objects.filter(user=instance).exists():
		new_invite_code = gen_invite_code()
		while UserReferral.objects.filter(invite_code=new_invite_code).exists():
			new_invite_code = gen_invite_code()
		UserReferral.objects.create(user=instance, invite_code=new_invite_code)

	print("Referral Profile Created")
	# print(sender, created, instance, created, args)



# @receiver(post_save, sender=UserReferral):