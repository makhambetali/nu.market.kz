from .models import *
from django import forms

choice = dict(Category.objects.values_list('id','name'))
print('aaaa', choice, Post.product_choice)
input_style = 'block w-full px-4 py-2.5 text-sm border-0 !bg-[#F0F0F0]'

class PostForm(forms.ModelForm):
    title = forms.CharField(required=True, label="item-name",
                    widget=forms.TextInput(attrs={'class': input_style + ' rounded-full',
                                                  'placeholder': 'Name'}))
    
    content = forms.CharField(required=True, label="description",
                    widget=forms.Textarea(attrs={'class': input_style + ' rounded-2xl',
                                                  'placeholder': 'Description'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="category",
        widget=forms.Select(
            attrs={'class': input_style + ' rounded-full', 'placeholder': 'Category'}
        )
    )
    
    condition = forms.ChoiceField(required=True, 
        choices=Post.product_choice,
        label="condition",
        widget=forms.Select(
            attrs={'class': input_style + ' rounded-full', 'placeholder': 'Condition'}))
    
    block = forms.ChoiceField(required=True, 
        choices=Post.block_choice,
        label="block",
        widget=forms.Select(
            attrs={'class': input_style + ' rounded-full', 'placeholder': 'Block'}))
    
    
    
    class Meta:
        model = Post
        exclude = ['creator']
        
