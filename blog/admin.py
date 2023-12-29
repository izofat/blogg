from django.contrib import admin
from .models import Post , Announcement


class PostAdmin(admin.ModelAdmin):
    list_display =('id', 'title', 'content' , 'datePosted' ,'author')

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id' , 'title' , 'context' , 'datePosted'  , 'author')

admin.site.register(Post , PostAdmin)
admin.site.register(Announcement, AnnouncementAdmin)