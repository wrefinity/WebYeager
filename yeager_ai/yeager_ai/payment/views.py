from typing import Any, Dict
import stripe
from yeager_ai.payment.models import Payment, Invoice
from django.conf import settings
from django.contrib import auth, messages
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, DeleteView, View, ListView, TemplateView
from djstripe.models import Product, Price, BalanceTransaction
from yeager_ai.user_profile.models import CreditModel


'''
get defined product model from djstrip dashboard
'''
class PriceView(LoginRequiredMixin, View):
    login_url = "/accounts/login"
    template_name = "pages/World/world_pricing.html",

    def get(self, request,  *args, **kwargs):
        price = Price.objects.all()
        return render(request, self.template_name, {'price': price})

    def post(self, request,  *args, **kwargs):
        pass

pricing_list_view = PriceView.as_view()


# Test Card Details.
# 4242 4242 4242 4242 dumy data card
# 12/34
# Use any three-digit CVC (four digits for American Express cards).

@csrf_exempt
def create_checkout_session(request, uuid):
    print("caller dispatced")
    if request.method == "POST":
        user = request.user
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        # stripe.Price.list()
        price = stripe.Price.retrieve(uuid)
        product = get_object_or_404(Product, id=price['product'])
        amount = price.unit_amount
        request.session['amount'] = amount
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                payment_method_types=['card'],
                line_items=[
                    {
                        'quantity': 1,
                        'name': product.name,
                        'amount': amount,
                        'currency': price.currency,
                    }
                ],

                mode='payment',
                customer_creation='always',
                success_url=request.build_absolute_uri(
                    reverse('payment:payment_success')
                ) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(
                    reverse('payment:payment_failed')),
            )

            payment = Payment()
            # payment.ref_number = field_uuid
            payment.customer_email = request.user.email
            payment.payment_intent = checkout_session['payment_intent']
            payment.amount = 200
            payment.user = request.user
            payment.payment_method_types = "card"
            payment.save()

            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print("Exception Meessages : ", e)
            messages.error(request, e)
            return HttpResponse({'error': str(e)})
    else:
        return render(request, 'pages/World/world_pricing.html')

class PaymentCreateView(LoginRequiredMixin, TemplateView):
    model = Payment
    login_url = "/accounts/login"
    template_name = "payments/create_payment.html"


payment_create_view = PaymentCreateView.as_view()

'''
get all payments made
applicable by admim
'''
class PaymentListView(LoginRequiredMixin, ListView):
    model = BalanceTransaction
    login_url = "/accounts/login"
    template_name = "payments/payment_list.html"
    context_object_name = 'payment_list'


payment_list_view = PaymentListView.as_view()

'''
get a specific user payments
'''
class PaymentUserView(LoginRequiredMixin, ListView):
    model = Payment
    login_url = "/accounts/login"
    template_name = "payments/payment_list.html"
    context_object_name = 'payment_list'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(PaymentListView, self).get_context_data(**kwargs)
        context["payments"] = get_object_or_404(
            Payment, user=self.request.user)
        return context


my_payment_view = PaymentUserView.as_view()

'''
get a particular payment 
details
'''
class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = "payments/payment_detail.html"
    login_url = "/accounts/login"

    def get_context_data(self, **kwargs):
        context = super(PaymentDetailView, self).get_context_data(**kwargs)
        payment = get_object_or_404(Payment, id=self.kwargs['id'])
        context['payment'] = payment
        return context


payment_detail_view = PaymentDetailView.as_view()


'''
An Endpoint for successful payments
'''
class PaymentSuccessView(LoginRequiredMixin, DetailView):
    template_name = "pages/Utils/Sucess.html"
    login_url = "/accounts/login"
    

    def get_object(self, queryset=None):
        session_id = self.request.GET.get('session_id', None)
        if session_id is None:
            messages.error(self.request, "session id is none")
            return reverse_lazy('payment:payment_checkout_session')

        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        customer = stripe.Customer.retrieve(session.customer)


        payment = Payment.objects.get(payment_intent=session.payment_intent, user=self.request.user)
        if payment:
            payment.has_paid = True
            payment.save()

        amount = self.request.session['amount']
        if self.request.session['amount']:
            user_account, created = CreditModel.objects.get_or_create(
            user=self.request.user)
            user_account.add_credit(float(amount))
            del self.request.session['amount']
        return render(self.request, self.template_name, {'customer': customer})


payment_success_view = PaymentSuccessView.as_view()


class PaymentFailedView(LoginRequiredMixin, TemplateView):
    login_url = "/accounts/login"
    template_name = "pages/Utils/payment_failed.html"


payment_failed_view = PaymentFailedView.as_view()


'''
Invoice Instance Section
Expectation invoices are created during payment and hence 
requires no create view 
'''
class InvoiceDetail(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "pages/Invoice/invoice_detail.html"
    login_url = "/accounts/login"


invoice_detail_view = InvoiceDetail.as_view()


class InvoiceListView(ListView, LoginRequiredMixin):
    model = Invoice
    login_url = "/accounts/login"
    template_name = "pages/Invoice/invoice_lists.html"
    context_object_name = 'invoice_list'
    paginate_by = 50


invoice_list_view = InvoiceListView.as_view()


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice_list")
    login_url = "/accounts/login"


invoice_delete_view = InvoiceDeleteView.as_view()

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)
