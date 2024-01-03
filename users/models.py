"""Models"""
from typing import Tuple
from django.db import models
from PIL import Image
from django.contrib.auth.models import User


class Profile(models.Model):
    """Profile for users that they can change their informations"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self) -> str:
        return f"{self.user.username} Profile"

    def save(self, *args: any, **kwargs: any) -> None:
        super(Profile, self).save(*args, **kwargs)
        img: Image.Image = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size: Tuple[int, int] = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
