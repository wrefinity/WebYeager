from django.test import TestCase
from yeager_ai.users.models import User
from django.urls import reverse

'''
Test Cases
1. upon user registration a referal relation is to be created 
2. user is to have 0.0 token assert this
3. upon referals user token is to increase
'''
class ReferalUrlTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')  
        
    def test_my_agent_view(self):
        response = self.client.get(reverse('api_my_agent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/agents/agent_list.html')
        self.assertEqual(response.context['agents'], self.agent)         

    def test_referral_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('referrals:view-referral-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/Referrals/referral.html')

    def test_referral_profile_view_unauthenticated(self):
        url = reverse('referrals:view-referral-profile')
        response = self.client.get(url)
        self.assertRedirects(response, '/accounts/login/?next=' + url)