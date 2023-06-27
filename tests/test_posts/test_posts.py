from django.test import TestCase
from posts.models import Post, Reply
from useraccounts.models import UserAccount

class PostTest(TestCase):
    
    def setUp(self):
        create_new_user1 = UserAccount.objects.create(
            username = 'testuser2',
            password = 'testpassword',
            user_slug = 'testuser2',
        )
        create_new_user1.save()

        get_new_user1 = list(UserAccount.objects.filter(username='testuser2'))[0]
        create_new_post1 = Post.objects.create(
            title = 'new post 1',
            content = 'new post 1 contents',
            user = get_new_user1,
            post_slug = 'new-post-1',

        )
        create_new_post1.save()

        get_new_post1 = list(Post.objects.filter(post_slug='new-post-1'))[0]
        create_new_reply1 = Reply.objects.create(
            content = 'new reply 1 content',
            user = get_new_user1,
            post_id = get_new_post1,

        )
        create_new_reply1.save()

        get_new_reply1 = list(Reply.objects.filter(content='new reply 1 content'))[0]
        create_new_reply_to_another_reply1 = Reply.objects.create(
            content = 'new reply 1 to another reply',
            user = get_new_user1,
            post_id = get_new_post1,
            reply_id = get_new_reply1,

        )
        create_new_reply_to_another_reply1.save()

    
    def test_new_post(self):
        new_post = list(Post.objects.filter(post_slug='new-post-1'))
        self.assertTrue(new_post)

    def test_new_reply(self):
        get_new_user1 = list(UserAccount.objects.filter(username='testuser2'))[0]
        new_reply = list(Reply.objects.filter(user=get_new_user1))
        self.assertTrue(new_reply)


    def test_reply_to_another_reply(self):
        get_new_reply1 = list(Reply.objects.filter(content='new reply 1 content'))[0]
        new_reply_to_anther_reply = list(Reply.objects.filter(reply_id=get_new_reply1))
        self.assertTrue(new_reply_to_anther_reply)