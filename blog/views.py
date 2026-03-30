from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import PostForm, Registration_Form
from django.core.paginator import Paginator
from .models import Post
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer


# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-id", "-created_at"]
    paginate_by=2
# First API View
class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class AboutView(TemplateView):
    template_name = "blog/about.html"


class ContactView(TemplateView):
    template_name = "blog/contact.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_details.html"
    context_object_name = "post"


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create_post.html"
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        messages.success(self.request, "Post Created Successfully")
        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/edit_post.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "id"
    def form_valid(self, form):
        messages.success(self.request, "Post Updated Successfully")
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "id"
    def form_valid(self, request, *args,**kwargs):
        messages.success(self.request, "Post Deleted Successfully")
        return super().delete(request,*args,**kwargs)


class RegisterView(CreateView):
    model = User
    form_class = Registration_Form
    template_name = "blog/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# Function-based views are kept here for reference (commented out)
"""
from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {"posts": posts}
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


# Post Details get by id

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_details.html', {"post": post})


# Form view
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})


# Edit Post View
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/edit_post.html", {"form": form})


# Delete Post
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect("home")


# Register User
def register(request):
    if request.method == "POST":
        form = Registration_Form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = Registration_Form()
    return render(request, "blog/register.html", {"form": form})
"""
