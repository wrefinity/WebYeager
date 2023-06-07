from django.urls import path
from .views import payment_create_view, payment_list_view, payment_detail_view, \
    payment_success_view, payment_failed_view, invoice_detail_view, invoice_list_view, \
    invoice_delete_view, create_checkout_session, my_payment_view, pricing_list_view

app_name = "payment"
urlpatterns = [
    path('list', payment_list_view, name="payment_list"),
    path('create', payment_create_view, name="payment_create"),
    path('failed', payment_failed_view, name="payment_failed"),
    path('success', payment_success_view, name="payment_success"),
    path('payment/<int:id>/', payment_detail_view, name="detail"),
    path('my_list', my_payment_view, name="payment_my_list"),
    path('checkout-session/<str:uuid>/', create_checkout_session, name='payment_checkout_session'),
    # invoice
    path('invoice/list', invoice_list_view, name="invoice_list"),
    path('invoice/<str:uuid>/', invoice_detail_view, name="invoice_detail"),
    path('invoice/delete/<str:uuid>/', invoice_delete_view, name="invoice_delete"),
    
    # pricing
    path('pricings', pricing_list_view, name="world_pricing"),   
]
