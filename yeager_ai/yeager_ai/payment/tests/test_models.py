from django.test import TestCase
from ..models import Payment
from yeager_ai.users.models import User
from django.urls import reverse, reverse_lazy

'''
Cases: 
1. user must be created
2. get plans
3. create payment with pending state
4. on payment success check intent on update
'''
class PaymentModelTestCase(TestCase):
    
    @classmethod
    def setUp(self):
        self.user = User.objects.create(username="TestUsername", name="TestUser", password="pxyrhrwy@1", first_name="FirstTestName",
                                   last_name="LastTestName", email="test@test.com", is_staff=False, is_admin=False, karma=0)
        self.payment = Payment.objects.create(user=self.user, amount=36, ref_number="1123XXX", payment_method_types="card", payment_intent="xcdxdddd", 
                               has_paid=False, description="User 2 payments")

    def test_payments_not_completed(self):
        """test for incomplete payments"""
        payment = Payment.objects.get(payment_intent="xcdxdddd")
        self.assertEquals(payment.has_paid, False)
        
    def test_payments_completed(self):
        """test for incomplete payments"""
        payment = Payment.objects.get(payment_intent="xcdxdddd")
        payment.has_paid = True
        payment.save()
        self.assertEquals(payment.has_paid, True)