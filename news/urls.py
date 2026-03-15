from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('<int:id>/', views.news_detail, name='news_detail'),
    path('create/', views.create_news_post, name='create_news_post'),
    path('<int:id>/edit/', views.edit_news_post, name='edit_news_post'),
    path('<int:id>/delete/', views.delete_news_post, name="delete_news_post"),
]