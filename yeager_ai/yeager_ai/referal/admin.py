from django.contrib import admin
from .models import UserReferral, ReferralEarning

# Register your models here.

class UserReferralAdmin(admin.ModelAdmin):
	print("admin loaded")
	# list_display = ("user", "invite_code", "referred_by" )
	empty_value_display = "-"
	list_display = ("user", "invite_code", "earnings", "invite_count", "invited_by", "date_invited" )

	class Meta:
		ordering = ("-created")

	def user(self, obj):
		return f"{obj.user.first_name} f{obj.user.last_name}"

	def date_invited(self, obj):
		if obj.invited_by:
			return obj.created
		return None

	def invite_count(self, obj):
		return obj.get_referred_by_me().count()


class ReferralEarningAdmin(admin.ModelAdmin):
	empty_value_display = "-"
	list_display = ('profile', 'earned_points', 'source', 'amount', 'date_earned')

	# def user(self, obj):
	# 	return f"{obj.profile.userfirst_name} f{obj.profile.last_name}"

	def source(self, obj):
		return f"{obj.source.first_name} f{obj.source.last_name}"


admin.site.register(UserReferral, UserReferralAdmin)
admin.site.register(ReferralEarning, ReferralEarningAdmin)