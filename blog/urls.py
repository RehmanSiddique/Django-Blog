


from django.urls import path
from  . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views. about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Single Post Details
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    # Create Post Form Route
    path("create-post/",views.create_post, name="create_post")
]
