from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsHomeView.as_view(), name='news_home'),
    path('<int:id>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('create/', views.CreateNewsPostView.as_view(), name='create_news_post'),
    path('<int:id>/edit/', views.EditNewsPostView.as_view(), name='edit_news_post'),
    path('<int:id>/delete/', views.DeleteNewsPostView.as_view(), name="delete_news_post"),
]