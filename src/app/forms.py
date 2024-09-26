from .models import *
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['creator']
        widgets = {
            
            # 'price': forms.TextInput(attrs={'oninput':'length_slice(this, 9)', 'class': 'currency-input'})

        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
           'image':forms.FileInput(attrs={'onchange':'previewImage(this)',"accept":"image/png, image/jpeg"})


        }
# class PostImageForm(forms.ModelForm):
#     class Meta:
#         model = PostImage
#         fields = ['image']
#         widgets = {
#             'image': forms.ClearableFileInput(attrs={'multiple': True}),
#         }