"""Models"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """A model for user that can post update delete"""

    title: models.CharField = models.CharField(max_length=100)
    content: models.TextField = models.TextField()
    datePosted: models.DateTimeField = models.DateTimeField(default=timezone.now)
    author: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Sets the display name of this object"""
        return self.title

    def get_absolute_url(self) -> str:
        """Creates a url for this post to reach it's details"""
        return reverse("post-detail", kwargs={"pk": self.pk})


class Announcement(models.Model):
    """A model for admins to make announcements to the users"""

    title: models.CharField = models.CharField(max_length=50)
    context: models.TextField = models.TextField()
    datePosted: models.DateTimeField = models.DateTimeField(default=timezone.now)
    author: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Sets the display name of this object"""
        return self.title
