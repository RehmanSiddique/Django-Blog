from django.urls import path
from  . import views 

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Single Post Details
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # Create Post Form Route
    path("create-post/", views.CreatePostView.as_view(), name="create_post"),
    # Edit Post Url
    path("post/edit/<int:id>/", views.EditPostView.as_view(), name="edit_post"),
    # Delete Post Url
    path("post/delete/<int:id>/", views.DeletePostView.as_view(), name="delete_post"),
    
    # Register User
    path("register/", views.RegisterView.as_view(), name="register")
]
