from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
import unittest  


class UserTest(TestCase):
    def setUp(self):
        user =  User.objects.create(username = 'cccc' , email = 'abc@gmail.com')
        user.set_password('abc12345')
        user.save()
    def test_user_created(self):
        user = User.objects.get(username = 'cccc')
        profile = Profile.objects.get(user = user)
        self.assertEqual(user.email  , 'abc@gmail.com')
        self.assertEqual(user.check_password('abc12345') , True)
        self.assertEqual(profile.user , user)
        self.assertEqual(profile.image.name , 'default.png')



if __name__ == '__main__':
    unittest.main()