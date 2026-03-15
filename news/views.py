from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsPost
from .forms import NewsPostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def news_home(request):
    news_posts = NewsPost.objects.all().order_by('-created_at')
    context = {
        "news_posts": news_posts
    }
    return render(request, 'news/news_home.html', context)
# News Details

def news_detail(request, id):
    news_post = get_object_or_404(NewsPost, id=id)
    return render(request, 'news/news_detail.html', {"news_post": news_post})


# create News Post first login required
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

# Edit News Post
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

# Delete News Post
@login_required
def delete_news_post(request, id):
    news_post = get_object_or_404(NewsPost, id=id)
    if request.method == "POST":
        news_post.delete()
        return redirect("news_home")
    return render(request, "news/delete_news_post.html", {"news_post": news_post})
    
