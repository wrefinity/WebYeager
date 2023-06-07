class ReferralMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response


	def __call__(self, request):
		if not request.user.is_authenticated:
			invite_code = request.GET.get("invite_code", None)
			if invite_code:
				request.session['invite_code'] = invite_code
		response = self.get_response(request)
		return response
