from django.test import TestCase
from useraccounts.models import UserAccount, Relation

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

        user1 = list(UserAccount.objects.filter(username='testuser1'))[0]
        user2 = list(UserAccount.objects.filter(username='testuser2'))[0]

        from_user1_to_user2 = Relation.objects.create(
            from_user = user1,
            to_user = user2
        )
        from_user1_to_user2.save()

        from_user2_to_user1 = Relation.objects.create(
            from_user = user2,
            to_user = user1
        )
        from_user2_to_user1.save()


    def test_relation(self):
        user1 = list(UserAccount.objects.filter(username='testuser1'))[0]
        user2 = list(UserAccount.objects.filter(username='testuser2'))[0]

        relation = Relation.objects.filter(from_user=user1, to_user=user2)
        self.assertTrue(relation)

        relation = Relation.objects.filter(from_user=user2, to_user=user1)
        self.assertTrue(relation)

    def test_following(self):
        user1 = list(UserAccount.objects.filter(username='testuser1'))[0]
        user2 = list(UserAccount.objects.filter(username='testuser2'))[0]

        self.assertEqual(UserAccount.following(user1), 1)
        self.assertEqual(UserAccount.following(user2), 1)

    def test_follower(self):
        user1 = list(UserAccount.objects.filter(username='testuser1'))[0]
        user2 = list(UserAccount.objects.filter(username='testuser2'))[0]

        self.assertEqual(UserAccount.follower(user1), 1)
        self.assertEqual(UserAccount.follower(user2), 1)

