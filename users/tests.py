# pylint: disable=relative-beyond-top-level
"""Tests"""
import os
from typing import Any, List

from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.views import LoginView
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpRequest
from django.views import View
from .models import Profile
from . import views


class UserTest(TestCase):
    """Test for user model"""

    def setUp(self) -> None:
        self.user: User = User.objects.create(
            username="cccc", email="abc@gmail.com", first_name="aaa", last_name="kkk"
        )
        self.user.set_password("abc12345")
        self.user.save()

    def test_user_created(self) -> None:
        """Checks the user is created after registeration"""
        self.assertEqual(self.user.email, "abc@gmail.com")
        self.assertEqual(self.user.check_password("abc12345"), True)
        self.assertEqual(self.user.first_name, "aaa")
        print("test_user_created is ok")

    def test_profile_created(self) -> None:
        """Checks the profile auto created after registeration"""
        profile: Profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.image.name, "default.png")
        print("test_profile_created is ok")


class URLTest(TestCase):
    """Test for urls in the users app"""

    def test_urls_resolved(self) -> None:
        """Checks the urls is giving the expected view"""
        url_names: List[str] = [
            "login",
            "logout_user",
            "logout_view",
            "register",
            "profile",
            "reset-password",
        ]
        view_names: List[str] = [
            "LoginView",
            "logout_user",
            "logout_view",
            "register_user",
            "profile",
            "reset_password",
        ]
        for i, url_name in enumerate(url_names):
            view_name: str = view_names[i]

            url: str = reverse(url_name)
            if url_name == "login":
                resolved_view: Any = resolve(url).func.view_class
                expected_view: Any = LoginView
            else:
                resolved_view: Any = resolve(url).func
                expected_view: Any = getattr(views, view_name, None)

            with self.subTest(url_name=url_name):
                self.assertEqual(resolved_view, expected_view)
        print("test_urls_resolved is ok")


class ViewTest(TestCase):
    """Tests for view and forms in the users app"""

    def setUp(self) -> None:
        self.client: Client = Client()
        self.user: User = User.objects.create(
            username="testusernametestusername", email="abc@gmail.com"
        )
        self.user.set_password("abc12345")
        self.user.save()

    def test_view_register(self) -> None:
        """Tests the register view"""
        url: str = reverse("register")
        response_get: HttpRequest = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        username: str = "kkkkkkk"

        response_post: HttpRequest = self.client.post(
            url,
            {
                "username": username,
                "email": "abc@gmail.com",
                "password1": "abcabc12",
                "password2": "abcabc12",
            },
        )
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse("login"))
        print("test_view_register is ok")

    def test_view_login(self) -> None:
        """Tests the login"""
        url: str = reverse("login")
        response_get: HttpRequest = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        response_post: HttpRequest = self.client.post(
            url, {"username": "testusernametestusername", "password": "abc12345"}
        )
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse("blog-home"))
        print("test_view_login is ok")

    def test_view_logout(self) -> None:
        """Tests the logout"""
        self.client.force_login(self.user)
        url: str = reverse("logout_user")
        response_get: HttpRequest = self.client.get(url)
        self.assertEqual(response_get.status_code, 302)

        print("test_view_logout is ok")

    def test_view_profile(self) -> None:
        """Tests the profile for updating and creating"""
        self.client.force_login(self.user)
        url: str = reverse("profile")
        response_get: HttpRequest = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        file_path: str = os.path.join(settings.MEDIA_ROOT, "test.png")
        with open(file_path, "rb") as picture:
            image: bytes = SimpleUploadedFile(
                "test.png", picture.read(), content_type="image/png"
            )
        response_post: HttpRequest = self.client.post(
            url,
            {
                "username": "testusernameaaaaa",
                "email": "aaa1234@gmail.com",
                "first_name": "ka",
                "last_name": "aaa",
                "image": image,
            },
        )
        self.assertEqual(response_post.status_code, 302)
        profile: Profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, "testusernameaaaaa")
        self.assertEqual(profile.user.email, "aaa1234@gmail.com")
        self.assertEqual(profile.user.first_name, "ka")
        self.assertEqual(profile.user.last_name, "aaa")
        self.assertTrue("test" in profile.image.name)
        print("test_view_profile is ok")

    def test_view_reset_password(self) -> None:
        """Tests the reset password view"""
        ##! login for not to redirect login
        self.client.force_login(self.user)
        url: str = reverse("reset-password")
        response_get: HttpRequest = self.client.get(url)

        self.assertEqual(response_get.status_code, 200)

        response_post: HttpRequest = self.client.post(
            url,
            {
                "old_password": "abc12345",
                "new_password1": "abc12345678910",
                "new_password2": "abc12345678910",
            },
        )
        updated_user: User = User.objects.get(id=self.user.id)
        self.assertTrue(updated_user.check_password("abc12345678910"))
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse("blog-home"))
        print("test_view_reset_password is ok")
