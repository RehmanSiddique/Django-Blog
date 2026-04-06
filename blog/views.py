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
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from .serializers import PostSerializer


# Create your views here.
# Class-based views for the blog application to handle different functionalities such as displaying the list of posts, post details, creating a new post, editing a post, deleting a post, and user registration. Additionally, API views are implemented to provide endpoints for retrieving the list of posts and post details in JSON format.
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-id", "-created_at"]
    paginate_by=2
# First API View
class PostListAPIView(APIView):
    # Get method for API to retrieve the list of all posts in JSON format and it will return the list of posts in JSON format with the status code 200 if the request is successful otherwise it will return an error message in JSON format with the appropriate status code
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    # Post method for API to create a new post by providing the post details in the request body in JSON format and it will return the created post details in JSON format if the post is created successfully otherwise it will return the validation errors in JSON format
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     # Put method for API to update the entire post details by providing all the fields in the request body and it will replace the existing post details with the new details provided in the request body 
class PostDetailAPI(APIView):
    # Helper method to get the post object based on the provided post id in the URL and if the post with the given id does not exist then it will return None

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None
#  Get method for API to retrieve the details of a single post by providing the post id in the URL and it will return the post details in JSON format
    def get(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Post not found"}, status=404)

        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # Put method for API to update the entire post details by providing all the fields in the request body and it will replace the existing post details with the new details provided in the request body

    def put(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Post not found"}, status=404)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
# Patch method for API to update only specific fields of the post without affecting other fields
    def patch(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Post not found"}, status=404)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    # Delete method for API

    def delete(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Post not found"}, status=404)

        post.delete()
        return Response({"message": "Post deleted successfully"}, status=204)




#  # LIST + CREATE
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# RETRIEVE + UPDATE + DELETE
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# 
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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
