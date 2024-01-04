# pylint: disable=relative-beyond-top-level

"""/"""
from typing import Any, Dict, List
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Announcement


class PostListView(ListView):
    """Shows all the post in the main page"""

    model: type = Post
    template_name: str = "blog/home.html"  # default <app>/<model>_<viewtype>.html
    context_object_name: str = "posts"
    ordering: List[str] = ["-datePosted"]
    paginate_by: int = 5

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["title"]: str = "Home"
        return context


class UserPostListView(ListView):
    """Shows all the posts of an user"""

    model: type = Post
    template_name: str = "blog/allpostuser.html"
    context_object_name: str = "posts"
    paginate_by: int = 5

    def get_queryset(self) -> QuerySet[Post]:
        self.user: User = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=self.user).order_by("-datePosted")

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["title"]: str = f"Posts of {self.user}"
        return context


class PostDetailView(DetailView):
    """Shows the details of a spesific post"""

    model: type = Post
    context_object_name: str = "post"

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["title"]: str = "Detail"
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """View to creating post"""

    model: type = Post
    fields: List[str] = ["title", "content"]

    def form_valid(self, form) -> HttpResponse:
        form.instance.author: User = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["form_type"]: str = "Create"
        context["title"]: str = "Create Post"
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to updating post"""

    model: type = Post
    fields: List[str] = ["title", "content"]

    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) -> bool:
        post: Post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["form_type"]: str = "Update"
        context["title"]: str = "Update Post"
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to deleting post"""

    model: type = Post
    success_url: str = "/"
    context_object_name: str = "post"

    def test_func(self) -> bool:
        post: bool = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["title"]: str = "Delete Post"
        return context

class LatestPostsView(ListView):
    """Shows the last 4 for post posted"""

    model: type = Post
    template_name: str = "blog/latest_posts.html"
    context_object_name: str = "latest_posts"

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.all().order_by("-datePosted")[:4]

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["title"]: str = "Latest Posts"
        return context


class AnnouncementsView(ListView):
    """Shows the announcements that admins announce"""

    model: type = Announcement
    template_name: str = "blog/announcements.html"
    context_object_name: str = "announcements"

    def get_context_data(self, **kwargs) -> Dict[Any, Any]:
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["title"]: str = "Announcements"
        return context
