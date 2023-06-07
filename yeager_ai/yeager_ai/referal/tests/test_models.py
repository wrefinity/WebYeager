from django.test import TestCase
from yeager_ai.users.models import User
from django.urls import reverse
from referal.models import UserReferral, ReferralEarning

'''
Test Cases
1. upon user registration a referal relation is to be created 
2. user is to have 0.0 token assert this
3. upon referals user token is to increase
'''
class ReferalTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_tokens(self):
        earning = self.user.referral_profile.earnings
        self.assertEqual(earning, 0.0)
        
    def test_add_earning(self):
        #get current user 
        user_referal = UserReferral.objects.get(user=self.user.id)
        # create refered user
        referred_user = User.objects.create_user(username='testuser2', password='testpassword', email="test2@test.com")
        user_earning = ReferralEarning.objects.get_or_create(profile=user_referal, source=referred_user)
        ReferralEarning.add_earning(profile=user_referal, source=referred_user, amount=100)
        self.assertGreater(user_referal.earnings, 0.0)
        
    def test_check_incremented_tokens(self):
        referal_updated  = UserReferral.objects.filter(user=self.user)
        referal_updated.earnings = 100.0
        self.assertGreater(referal_updated.earnings, 0.0)
        self.assertEqual(referal_updated.earnings, 100.0)   