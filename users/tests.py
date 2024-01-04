# pylint: disable=relative-beyond-top-level
"""Tests"""
import os
from typing import Any, List
from faker import Faker
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.views import LoginView
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpRequest
from django.views import View
from .models import Profile , UserFactory 
from . import views


class UserTest(TestCase):
    """Test for user model"""

    def setUp(self) -> None:

        self.user: User = UserFactory.create()
        self.user.set_password("abc12345")
        self.user.save()

    def test_user_created(self) -> None:
        """Checks the user is created after registeration"""
        user_created = User.objects.get(id = self.user.id)
        self.assertEqual(self.user.email, user_created.email)
        self.assertTrue(user_created.check_password("abc12345"))
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
        self.user: User = UserFactory.create()
        self.user.set_password("abc12345")
        self.user.save()
        

    def test_view_register(self) -> None:
        """Tests the register view"""
        url: str = reverse("register")
        response_get: HttpRequest = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        faker = Faker()
        self.faker_password = faker.password(length = 10)
        response_post: HttpRequest = self.client.post(
            url,
            {
                "username": faker.user_name(),
                "email": faker.email(),
                "password1": self.faker_password,
                "password2": self.faker_password,
            },
        )   
        self.assertTrue(User.objects.filter(id = self.user.id).exists())
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse("login"))
        print("test_view_register is ok")

    def test_view_login(self) -> None:
        """Tests the login"""
        url: str = reverse("login")
        response_get: HttpRequest = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
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
        faker = Faker()
        faker_username =  faker.user_name()
        faker_email = faker.email()
        faker_first_name = faker.first_name()
        faker_last_name = faker.last_name() 
        response_post: HttpRequest = self.client.post(
            url,
            {
                "username": faker_username,
                "email": faker_email,
                "first_name": faker_first_name,
                "last_name": faker_last_name,
                "image": image,
            },
        )
        self.assertEqual(response_post.status_code, 302)
        profile: Profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, faker_username)
        self.assertEqual(profile.user.email, faker_email)
        self.assertEqual(profile.user.first_name, faker_first_name)
        self.assertEqual(profile.user.last_name, faker_last_name)
        self.assertTrue("test" in profile.image.name)
        print("test_view_profile is ok")

    def test_view_reset_password(self) -> None:
        """Tests the reset password view"""
        ##! login for not to redirect login
        self.client.force_login(self.user)
        url: str = reverse("reset-password")
        response_get: HttpRequest = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        faker = Faker()
        faker_password_new = faker.password(length = 10) 
        response_post: HttpRequest = self.client.post(
            url,
            {
                "old_password": 'abc12345',
                "new_password1": faker_password_new,
                "new_password2": faker_password_new,
            },
        )
        updated_user: User = User.objects.get(id=self.user.id)
        self.assertTrue(updated_user.check_password(faker_password_new))
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse("blog-home"))
        print("test_view_reset_password is ok")
