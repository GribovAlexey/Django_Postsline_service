from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from .models import Post
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class HomeView(ListView):
    model = Post
    template_name = "home.html"


class ArticleDetailView(DetailView):
    model = Post
    template_name = "article_detail.html"


class AddPostView(CreateView):
    model = Post
    template_name = "add_post.html"
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ['title', 'content']


class DeletePostView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("home")
