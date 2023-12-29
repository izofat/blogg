
from typing import Any
from django.shortcuts import render , get_object_or_404
from .models import Post , Announcement
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'   # default <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-datePosted']
    paginate_by = 5
    
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/allpostuser.html'   
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-datePosted')

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post    
    fields = ['title' , 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs: Any) :
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'Create'
        return context
        
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title' , 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: 
            return True
        return False
    def get_context_data(self, **kwargs: Any) :
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'Update'
        return context
        
    
class PostDeleteView (LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = Post;
    success_url = '/'
    context_object_name = 'post'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: 
            return True
        return False


class LatestPostsView(ListView):
    model = Post
    template_name = 'blog/latest_posts.html'
    context_object_name = 'latest_posts'
    def get_queryset(self):
        return Post.objects.all().order_by('-datePosted')[:4]
    
class AnnouncementsView(ListView):
    model = Announcement
    template_name =  'blog/announcements.html'
    context_object_name = 'announcements'


