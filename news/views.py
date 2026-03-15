from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsPost
from .forms import NewsPostForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

# Function-based views (commented out)
"""
def news_home(request):
    news_posts = NewsPost.objects.all().order_by('-created_at')
    context = {
        "news_posts": news_posts
    }
    return render(request, 'news/news_home.html', context)

def news_detail(request, id):
    news_post = get_object_or_404(NewsPost, id=id)
    return render(request, 'news/news_detail.html', {"news_post": news_post})

@login_required
def create_news_post(request):
    if request.method == "POST":
        form = NewsPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("news_home")
    else:
        form = NewsPostForm()
    return render(request, "news/create_news_post.html", {"form": form})

@login_required
def edit_news_post(request, id):
    news_post = get_object_or_404(NewsPost, id=id)
    if request.method == "POST":
        form = NewsPostForm(request.POST, request.FILES, instance=news_post)
        if form.is_valid():
            form.save()
            return redirect("news_home")
    else:
        form = NewsPostForm(instance=news_post)
    return render(request, "news/edit_news_post.html", {"form": form})

@login_required
def delete_news_post(request, id):
    news_post = get_object_or_404(NewsPost, id=id)
    if request.method == "POST":
        news_post.delete()
        return redirect("news_home")
    return render(request, "news/delete_news_post.html", {"news_post": news_post})
"""

# Class-based views

class NewsHomeView(ListView):
    model = NewsPost
    template_name = 'news/news_home.html'
    context_object_name = 'news_posts'
    ordering = ['-created_at']

class NewsDetailView(DetailView):
    model = NewsPost
    template_name = 'news/news_detail.html'
    context_object_name = 'news_post'
    pk_url_kwarg = 'id'

class CreateNewsPostView(LoginRequiredMixin, CreateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = 'news/create_news_post.html'
    success_url = reverse_lazy('news_home')

class EditNewsPostView(LoginRequiredMixin, UpdateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = 'news/edit_news_post.html'
    success_url = reverse_lazy('news_home')
    pk_url_kwarg = 'id'

class DeleteNewsPostView(LoginRequiredMixin, DeleteView):
    model = NewsPost
    template_name = 'news/delete_news_post.html'
    success_url = reverse_lazy('news_home')
    pk_url_kwarg = 'id'
    context_object_name = 'news_post'
    
