from django.test import TestCase , Client
from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse , resolve
from . import views
from django.contrib.auth.views import LoginView
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings
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

class URLTest(TestCase):
    def test_urls_resolved(self):
        url_names = [ 'login' ,'logout_user' , 'logout_view'  , 'register' , 'profile' , 'reset-password']
        view_names = [ 'LoginView', 'logout_user' , 'logout_view' , 'register_user' ,'profile' ,'reset_password' ]
        for i in range(len(url_names)):
            url_name = url_names[i]
            view_name = view_names[i]

            url = reverse(url_name)
            if url_name == 'login':
                resolved_view = resolve(url).func.view_class
                expected_view = LoginView
            else:
                resolved_view = resolve(url).func
                expected_view = getattr(views , view_name , None)
            
            with self.subTest(url_name = url_name):
                self.assertEqual( resolved_view ,expected_view)

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user =  User.objects.create(username = 'testusernametestusername' , email = 'abc@gmail.com')
        self.user.set_password('abc12345')
        self.user.save()
    def test_view_register(self):
        url = reverse('register')
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code , 200)
        username = 'kkkkkkk'
        response_post = self.client.post(url , {'username' : username  , 'email' : 'abc@gmail.com'  , 'password1' : 'abcabc12' , 'password2' : 'abcabc12'})
        self.assertTrue(User.objects.filter(username = username).exists())        
        self.assertEqual(response_post.status_code , 302)
        self.assertRedirects(response_post , reverse('login'))

    def test_view_login(self):
        url = reverse('login')
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code , 200)
        response_post = self.client.post(url , {'username' : 'testusernametestusername' , 'password' : 'abc12345'})

        self.assertEqual(response_post.status_code , 302)
        self.assertRedirects(response_post , reverse('blog-home'))

    def test_view_logout(self):
        
        self.client.force_login(self.user)
        url = reverse('logout_user')
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code ,302)
    
    def test_view_profile(self):
        self.client.force_login(self.user)

        url = reverse('profile')
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code , 200)
        file_path = os.path.join(settings.MEDIA_ROOT , 'test.png')
        with open(file_path , 'rb') as picture :
            image = SimpleUploadedFile('test.png' , picture.read() , content_type='image/png')
        response_post = self.client.post(url , {'username' : 'testusernameaaaaa','email' : 'aaa1234@gmail.com'  , 'first_name' : 'ka' , 'last_name':'aaa', 'image' : image })
        self.assertEqual(response_post.status_code , 302)
        profile = Profile.objects.get(user = self.user)
        self.assertEqual(profile.user.username , 'testusernameaaaaa')
        self.assertEqual(profile.user.email , 'aaa1234@gmail.com')
        self.assertEqual(profile.user.first_name , 'ka')
        self.assertEqual(profile.user.last_name , 'aaa')
        self.assertTrue('test' in profile.image.name )

    def test_view_reset_password(self):
        ##! login for not to redirect login
        self.client.force_login(self.user)
        url = reverse('reset-password')
        response_get = self.client.get(url)

        self.assertEqual(response_get.status_code , 200)    

        response_post = self.client.post(url , {'old_password' : 'abc12345' , 'new_password1' : 'abc12345678910' , 'new_password2' : 'abc12345678910' })
        updated_user = User.objects.get(id = self.user.id)
        self.assertTrue(updated_user.check_password('abc12345678910'))
        self.assertEqual(response_post.status_code , 302)
        self.assertRedirects(response_post , reverse('blog-home'))
