from django.test import TestCase
from posts.models import Post
from useraccounts.models import UserAccount

class PostTest(TestCase):
    
    def setUp(self):
        new_user1 = UserAccount.objects.create(
            username = 'testuser2',
            password = 'testpassword',
            user_slug = 'testuser2',
        )
        new_user1.save()

        new_user1 = list(UserAccount.objects.filter(username='testuser2'))[0]
        new_post1 = Post.objects.create(
            title = 'new post 1',
            content = 'new post 1 contents',
            user = new_user1,
            post_slug = 'new-post-1',

        )
        new_post1.save()

    
    def test_new_post(self):
        new_post = Post.objects.all()
        self.assertTrue(new_post)