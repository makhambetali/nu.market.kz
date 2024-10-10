from .models import *
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['creator']
        
