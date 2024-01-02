from django.test import TestCase
import unittest
from .models import Post
from django.contrib.auth.models import User
from django.core import exceptions as exception


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = 'testuser' , email = 'aaa@gmail.com')
        self.user.set_password('aab12345')
        self.user.save()
        self.post =  Post.objects.create(title = 'thistestpost' , content = 'test post content' , author = self.user)
        self.post.save()
    def test_post_created(self):           
        self.assertEqual(self.post.title  , 'thistestpost')
        self.assertEqual(self.post.content , 'test post content')
        self.assertEqual(self.post.author , self.user)
        self.assertIsNotNone(self.post.datePosted)

    def test_post_updated(self):
        self.post.content = 'test post content updated'
        self.post.save()
        self.assertEqual(self.post.content  , 'test post content updated')
    
    def test_post_deleted(self):
        self.post.delete()
        with self.assertRaises(exception.ObjectDoesNotExist):
            Post.objects.get(title = 'thistestpost' , author = self.user)

     


