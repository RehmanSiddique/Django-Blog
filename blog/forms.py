from django import forms
from django.contrib.auth.models import User
# UserCreationForm is  built in Django Form
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']
        
        
# User Form Model
class Registration_Form(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]