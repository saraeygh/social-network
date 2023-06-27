from django.test import TestCase
from useraccounts.models import UserAccount

class UserAccountTest(TestCase):
    
    def setUp(self):        
        new_user1 = UserAccount.objects.create(
            username = 'testuser1',
            password = 'testpassword',
            user_slug = 'testuser1',

        )
        new_user1.save()

        new_user2 = UserAccount.objects.create(
            username = 'testuser2',
            password = 'testpassword',
            user_slug = 'testuser2',
        )
        new_user2.save()

    def test_create_user(self):
        registered_user = UserAccount.objects.filter(username='testuser2')
        self.assertTrue(registered_user)