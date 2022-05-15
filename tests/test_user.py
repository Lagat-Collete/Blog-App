import unittest

from app.models import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username='lagatmine',email = "mine33@gmail.com", bio ='default bio',password='mine1234')

    def test_password_setter(self):   
        self.assertTrue(self.new_user.password_hash , not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password_hash 

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password(''))
