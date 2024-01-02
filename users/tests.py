from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
import unittest  


class UserTest(TestCase):
    def setUp(self):
        self.user =  User.objects.create(username = 'cccc' , email = 'abc@gmail.com' , first_name='aaa' , last_name ='kkk')
        self.user.set_password('abc12345')
        self.user.save()
    def test_user_created(self):
        self.assertEqual(self.user.email  , 'abc@gmail.com')
        self.assertEqual(self.user.check_password('abc12345') , True)
        self.assertEqual(self.user.first_name , 'aaa')       
    def test_profile_created(self):
        profile = Profile.objects.get(user = self.user)
        self.assertEqual(profile.user , self.user)
        self.assertEqual(profile.image.name , 'default.png')


if __name__ == '__main__':
    unittest.main()