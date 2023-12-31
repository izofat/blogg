"""URls"""
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    LatestPostsView,
    AnnouncementsView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("allposts/<str:username>/", UserPostListView.as_view(), name="allposts-user"),
    path("post/latests", LatestPostsView.as_view(), name="posts-latest"),
    path("announcements/", AnnouncementsView.as_view(), name="announcements"),
]
