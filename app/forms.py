from app.models import *
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['creator']
        widgets = {
            
            'price': forms.TextInput(attrs={'oninput':'length_slice(this, 9)', 'class': 'currency-input'})

        }
