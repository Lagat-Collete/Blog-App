import unittest
from app.models import Comment, Post, User
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        
        self.new_comment = Comment(id = 1, comment = 'Test comment', user = self.user_lagatmine, post_id = self.new_post)
        
    def tearDown(self):
        Post.query.delete()
        User.query.delete()
    
    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'Test comment')
        self.assertEquals(self.new_comment.user,self.user_lagatmine)
        self.assertEquals(self.new_comment.post_id,self.new_post)


class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_lagatmine = User(username='lagatmine', password='mine1234', email='mine33@gmail.com')
        self.new_post = Post(id=1, title='Test', content='Post to be tested', user_id=self.user_lagatmine.id)
        self.new_comment = Comment(id=1, comment ='Test comment', user_id=self.user_lagatmine.id, post_id = self.new_post.id )

    def tearDown(self):
        Post.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment, 'Test comment')
        self.assertEquals(self.new_comment.user_id, self.user_lagatmine.id)
        self.assertEquals(self.new_comment.post_id, self.new_post.id)

    def test_save_comment(self):
        self.new_comment.save()
        self.assertTrue(len(Comment.query.all()) > 0)

    def test_get_comment(self):
        self.new_comment.save()
        get_comment = Comment.get_comment(1)
        self.assertTrue(get_comment is not None)