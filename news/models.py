from django.db import models

# Create your models here.

class NewsPost(models.Model):
    title=models.CharField(max_length=300)
    content=models.TextField()
    picture=models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
