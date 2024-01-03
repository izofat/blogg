from typing import Tuple
from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str] = ("id", "user", "image")


admin.site.register(Profile, ProfileAdmin)
