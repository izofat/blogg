# pylint: disable=relative-beyond-top-level
"""Admin page"""
from typing import Tuple
from django.contrib import admin
from .models import Post, Announcement


class PostAdmin(admin.ModelAdmin):
    """Sets the informations that will display in the admin panel for post"""

    list_display: Tuple[str, str] = ("id", "title", "content", "datePosted", "author")


class AnnouncementAdmin(admin.ModelAdmin):

    """Sets the informations that will display in the admin panel for announcement"""

    list_display: Tuple[str, str] = ("id", "title", "context", "datePosted", "author")


admin.site.register(Post, PostAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
