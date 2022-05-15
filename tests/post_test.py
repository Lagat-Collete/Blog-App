import unittest
from app.models import Post, User
from app import db

class PostModelTest(unittest.TestCase):
    def setUp(self):
        self.user_marie = User(username='lagatmine', password='mine1234', email='mine33@gmail.com')
        self.new_post = Post(id=1, title='Test', content='Post testing', user_id=self.user_lagatmine.id)

    def tearDown(self):
        Post.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title, 'Test')
        self.assertEquals(self.new_post.content, 'Post testing')
        self.assertEquals(self.new_post.user_id, self.user_marie.id)

    def test_save_post(self):
        self.new_post.save()
        self.assertTrue(len(Post.query.all()) > 0)

    def test_get_post(self):
        self.new_post.save()
        get_post = Post.get_post(1)
        self.assertTrue(get_post is not None)