from django.test import TestCase , Client
from django.urls import reverse , resolve
from . import views 
from .models import Post
from django.contrib.auth.models import User
from django.core import exceptions as exception
from django.contrib.auth.models import User

class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="aaa@gmail.com")
        self.user.set_password("aab12345")
        self.user.save()
        self.post = Post.objects.create(
            title="thistestpost", content="test post content", author=self.user
        )
        self.post.save()

    def test_post_created(self):
        self.assertEqual(self.post.title, "thistestpost")
        self.assertEqual(self.post.content, "test post content")
        self.assertEqual(self.post.author, self.user)
        self.assertIsNotNone(self.post.datePosted)
        print('test_post_created is ok')
    def test_post_updated(self):
        self.post.content = "test post content updated"
        self.post.save()
        self.assertEqual(self.post.content, "test post content updated")
        print('test_post_updated is ok')
    def test_post_deleted(self):
        self.post.delete()
        with self.assertRaises(exception.ObjectDoesNotExist):
            Post.objects.get(title="thistestpost", author=self.user)
        print('test_post_deleted is ok')

class URLTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = 'test' , email='a@gmail.com')
        self.user.set_password('aaa123123')
        self.post = Post.objects.create(title = 'aa' , content = 'aa' , author = self.user)

    def test_basic_urls_resolved_without_params(self):
        url_names = ['blog-home'  , 'post-create'  , 'posts-latest' , 'announcements']
        view_classes = ['PostListView'  , 'PostCreateView'  , 'LatestPostsView' , 'AnnouncementsView']
        for i in range(len(url_names)):
            url_name = url_names[i]
            view_class = view_classes[i]
            url =reverse(url_name)
            resolved_view = resolve(url).func.view_class
            expected_view = getattr(views ,view_class , None)
            with self.subTest(url_name = url_name):
                self.assertEqual(resolved_view , expected_view)
        print('test_basic_urls_resolved_without_params is ok')
    def test_urls_resolved_with_params(self):
        url_names = ['post-detail'  , 'post-update'  , 'post-delete' , 'allposts-user']
        view_classes = ['PostDetailView'  , 'PostUpdateView'  , 'PostDeleteView' , 'UserPostListView']
        for i in range(len(url_names)):
            url_name = url_names[i]
            view_class = view_classes[i]

            if url_name == 'allposts-user':
                url = reverse(url_name , kwargs={'username' : self.user.username} )
            else:
                url =reverse(url_name , kwargs={'pk' : self.post.id})
            
            resolved_view = resolve(url).func.view_class
            expected_view = getattr(views ,view_class , None)
            with self.subTest(url_name = url_name):
                self.assertEqual(resolved_view , expected_view)
        print('test_urls_resolved_with_params is ok')

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username = 'test' , email='a@gmail.com')
        self.user.set_password('aaa123123')
        self.post = Post.objects.create(title = 'aa' , content = 'aa' , author = self.user)
        self.client.force_login(self.user)
    def test_post_view_GET(self):
        url_names = ['blog-home' , 'posts-latest' , 'announcements' , 'post-detail' ,'allposts-user']
        template_names = ['home.html' , 'latest_posts.html' , 'announcements.html' , 'post_detail.html' , 'allpostuser.html']
        for i in range(len(url_names)):
            url_name = url_names[i]
            template_name = template_names[i]
            if url_name == 'post-detail':
                url = reverse(url_name , kwargs={'pk' : self.post.id})
            elif url_name == 'allposts-user':
                url = reverse(url_name , kwargs={'username' : self.user.username})
            else:
                url = reverse(url_name)
            
            response = self.client.get(url)
            self.assertEqual(response.status_code , 200)
            self.assertTemplateUsed(response , 'blog/' + template_name )
        print('test_post_view_GET is ok')

    def test_post_view_POST_create(self):
        url_create = reverse('post-create')
        response_create =  self.client.post(url_create , {'title' : 'aaa' , 'content' : 'bbb' , 'author' : self.user})
        self.assertEqual(response_create.status_code , 302)
        print('test_post_view_POST_create is ok')
    def test_post_view_POST_update(self):
        post1 = Post.objects.create(title = 'aaa' , content = 'bbb' , author = self.user)
        url_update = reverse('post-update' , kwargs={'pk' : post1.id})
        update_data = {'title' : 'kkk' ,  'content' : 'ppp'}
        response_update = self.client.post(url_update  , update_data)
        self.assertEqual(response_update.status_code , 302)
        print('test_post_view_POST_update is ok')
    def test_post_view_DELETE_delete(self):
        url_delete = reverse('post-delete' , kwargs={'pk' : self.post.id})
        response_get = self.client.get(url_delete)
        self.assertEqual(response_get.status_code , 302)

        response_delete = self.client.delete(url_delete)
        self.assertEqual(response_delete.status_code , 302)
        print('test_post_view_DELETE_delete is ok')
        
            
