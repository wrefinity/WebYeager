from django.test import TestCase
from django.urls import reverse, reverse_lazy, resolve
from yeager_ai.payment.views import payment_list_view
from yeager_ai.users.models import User


class PaymentURLTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_payment_list_url(self):
        url = reverse('payment:payment_list')
        self.assertEqual(url, '/payment/list')
        
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'payment:payment_list')
        
    def test_pricing_view_get(self):
        url = reverse('payment:world_pricing')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/World/world_pricing.html')
        
 
    def test_payment_success_view_get(self):
        url = reverse('payment:payment_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/Utils/Sucess.html')
