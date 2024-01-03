# pylint: disable=relative-beyond-top-level
"""Modules for testing"""
from typing import Any, Dict, List
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core import exceptions as exception
from django.contrib.auth.models import User
from . import views
from .models import Post


class PostTest(TestCase):
    """Tests Post model"""

    def setUp(self) -> None:
        self.user: User = User.objects.create(
            username="testuser", email="aaa@gmail.com"
        )
        self.user.set_password("aab12345")
        self.user.save()
        self.post: Post = Post.objects.create(
            title="thistestpost", content="test post content", author=self.user
        )
        self.post.save()

    def test_post_created(self) -> None:
        """Checks post is created"""

        self.assertEqual(self.post.title, "thistestpost")
        self.assertEqual(self.post.content, "test post content")
        self.assertEqual(self.post.author, self.user)
        self.assertIsNotNone(self.post.datePosted)
        print("test_post_created is ok")

    def test_post_updated(self) -> None:
        """Checks post is updated"""

        self.post.content: str = "test post content updated"
        self.post.save()
        self.assertEqual(self.post.content, "test post content updated")
        print("test_post_updated is ok")

    def test_post_deleted(self) -> None:
        """Checks post is deleted"""

        self.post.delete()
        with self.assertRaises(exception.ObjectDoesNotExist):
            Post.objects.get(title="thistestpost", author=self.user)
        print("test_post_deleted is ok")


class URLTest(TestCase):
    """Tests urls in blog"""

    def setUp(self) -> None:
        self.user: User = User.objects.create(username="test", email="a@gmail.com")
        self.user.set_password("aaa123123")
        self.post: Post = Post.objects.create(
            title="aa", content="aa", author=self.user
        )

    def test_basic_urls_resolved_without_params(self) -> None:
        """Cheks the urls that don't need a paramater to render"""

        url_names: List[str] = [
            "blog-home",
            "post-create",
            "posts-latest",
            "announcements",
        ]
        view_classes: List[str] = [
            "PostListView",
            "PostCreateView",
            "LatestPostsView",
            "AnnouncementsView",
        ]
        for i, url_name in enumerate(url_names):
            view_class: str = view_classes[i]
            url: str = reverse(url_name)
            resolved_view: Any = resolve(url).func.view_class
            expected_view: Any = getattr(views, view_class, None)
            with self.subTest(url_name=url_name):
                self.assertEqual(resolved_view, expected_view)
        print("test_basic_urls_resolved_without_params is ok")

    def test_urls_resolved_with_params(self) -> None:
        """Checks the urls that take paramater"""

        url_names: List[str] = [
            "post-detail",
            "post-update",
            "post-delete",
            "allposts-user",
        ]
        view_classes: List[str] = [
            "PostDetailView",
            "PostUpdateView",
            "PostDeleteView",
            "UserPostListView",
        ]
        for i, url_name in enumerate(url_names):
            view_class: str = view_classes[i]

            if url_name == "allposts-user":
                url: str = reverse(url_name, kwargs={"username": self.user.username})
            else:
                url: str = reverse(url_name, kwargs={"pk": self.post.id})

            resolved_view: Any = resolve(url).func.view_class
            expected_view: Any = getattr(views, view_class, None)
            with self.subTest(url_name=url_name):
                self.assertEqual(resolved_view, expected_view)
        print("test_urls_resolved_with_params is ok")


class ViewTest(TestCase):
    """Tests views in blog"""

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create(username="test", email="a@gmail.com")
        self.user.set_password("aaa123123")
        self.post = Post.objects.create(title="aa", content="aa", author=self.user)
        self.client.force_login(self.user)

    def test_post_view_get(self) -> None:
        """Checks views that just run with get request"""

        url_names: List[str] = [
            "blog-home",
            "posts-latest",
            "announcements",
            "post-detail",
            "allposts-user",
        ]
        template_names: List[str] = [
            "home.html",
            "latest_posts.html",
            "announcements.html",
            "post_detail.html",
            "allpostuser.html",
        ]
        for i, url_name in enumerate(url_names):
            template_name: str = template_names[i]
            if url_name == "post-detail":
                url: str = reverse(url_name, kwargs={"pk": self.post.id})
            elif url_name == "allposts-user":
                url: str = reverse(url_name, kwargs={"username": self.user.username})
            else:
                url: str = reverse(url_name)

            response: HttpRequest = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "blog/" + template_name)
        print("test_post_view_GET is ok")

    def test_post_view_post_create(self):
        """Checks the view and the form for creating post"""

        url_create: str = reverse("post-create")
        response_create: HttpRequest = self.client.post(
            url_create, {"title": "aaa", "content": "bbb", "author": self.user}
        )
        self.assertEqual(response_create.status_code, 302)
        print("test_post_view_POST_create is ok")

    def test_post_view_post_update(self):
        """Checks the view and the form for updating post"""

        post1: Post = Post.objects.create(title="aaa", content="bbb", author=self.user)
        url_update: str = reverse("post-update", kwargs={"pk": post1.id})
        update_data: Dict[str, str] = {"title": "kkk", "content": "ppp"}
        response_update: HttpRequest = self.client.post(url_update, update_data)
        self.assertEqual(response_update.status_code, 302)
        print("test_post_view_post_update is ok")

    def test_post_view_delete(self):
        """Checks the view and form for deleting post"""

        url_delete: str = reverse("post-delete", kwargs={"pk": self.post.id})
        response_get: HttpRequest = self.client.get(url_delete)
        self.assertEqual(response_get.status_code, 302)

        response_delete: HttpRequest = self.client.delete(url_delete)
        self.assertEqual(response_delete.status_code, 302)
        print("test_post_view_delete is ok")
