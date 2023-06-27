from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from posts.models import Post, Reply
from useraccounts.models import UserAccount
from tags.models import Tag, TaggedItem

class TagTest(TestCase):
    
    def setUp(self):
        create_new_tag1 = Tag.objects.create(
            label = 'testtag1',
        )
        create_new_tag1.save()

        create_new_user1 = UserAccount.objects.create(
            username = 'testuser1',
            password = 'testpassword',
            user_slug = 'testuser1',
        )
        create_new_user1.save()

        get_new_user1 = list(UserAccount.objects.filter(username='testuser1'))[0]
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


        get_new_tag = list(Tag.objects.filter(label='testtag1'))[0]
        get_post_content_type = list(ContentType.objects.filter(id=9))[0]
        get_user_content_type = list(ContentType.objects.filter(id=6))[0]
        set_tag_on_post1 = TaggedItem.objects.create(
            tag = get_new_tag,
            content_type = get_post_content_type,
            object_id = get_new_post1.id,
            tag_from = get_user_content_type,
            user = get_new_user1.id,

        )
        set_tag_on_post1.save()



    def test_create_tag(self):
        get_new_tag = list(Tag.objects.filter(label='testtag1'))
        self.assertTrue(get_new_tag)

    def test_tagged_item(self):
        get_new_tagged_item = list(TaggedItem.objects.all())
        self.assertTrue(get_new_tagged_item)

    def test_tag_used_count(self):
        get_new_tag = list(Tag.objects.filter(label='testtag1'))[0]
        self.assertEqual(Tag.used_count(get_new_tag), 1)

    