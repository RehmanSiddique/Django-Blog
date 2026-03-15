from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from .forms import PostForm

# Create your views here.

def home(request):
    posts=Post.objects.all().order_by('-created_at')
    

    context = {
        "posts": posts
    }
    return render(request,'blog/home.html',context)
def about(request):
    return render(request,'blog/about.html')
def contact(request):
    return render(request,'blog/contact.html')
#  Post Details get by id
def post_detail(request,id):
    post=get_object_or_404(Post, id=id)
    return render(request, 'blog/post_details.html', {"post":post})

# form View 
def create_post(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form=PostForm()
    return render(request, "blog/create_post.html", {"form":form})
#  Edit Post View

def edit_post(request,id):
    post=get_object_or_404(Post,id=id)
    if request.method=="POST":
        form=PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form=PostForm(instance=post)
    return render(request,"blog/edit_post.html", {"form":form})

# Delete Post

def delete_post(request,id):
    post=get_object_or_404(Post,id=id)
    post.delete()
    return redirect("home")