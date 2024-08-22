from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.forms import BaseModelForm
from app.models import *
from app.forms import *
from django.utils import timezone
from django.http import JsonResponse
def str_to_int(string):
    return int(''.join(filter(str.isdigit, string)))
# Create your views here.
# @login_required
# def homePage(request):
    
#     return render(request, 'dist/index.html')

def MessagePage(request):
    return render(request, 'dist/message.html')

def PostPage(request):
    return render(request, 'dist/post.html')


def ProfilePage(request):
    return render(request, 'dist/profile.html')


def LikedPage(request):
    return render(request, 'dist/liked.html')


def DetailsPage(request):
    return render(request, 'dist/details.html')

class HomePageView(LoginRequiredMixin, ListView):
    model = Post

    template_name = 'dist/home.html'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()

        return context
    


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'dist/post.html'
    success_url = reverse_lazy('app:home-page')
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            form = form.save(commit=False)
            
            form.creator = request.user
            price = request.POST.get('price')
            form.price = str_to_int(price)
            
            form.save()
            images = self.request.FILES.getlist('files')
            print('images', images)
            for index in range(len(images)):
                print('1')
                PostImage.objects.create(image = images[index], post = form, is_primary = bool(index==0) )
            messages.success(
                self.request,
                f'Пост успешно добавлен.'
            )
            return redirect('app:home-page')
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print(form.errors)
        return HttpResponse('Form is invalid')
        return super().form_invalid(form)

    
class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'dist/post.html'
    success_url = reverse_lazy('app:home-page')
    def form_valid(self, form):
        form_instance = form.save(commit=False)
        price = str_to_int(self.request.POST.get('price'))
        form_instance.creator = self.request.user
        form_instance.price = price
        form_instance.save()

        messages.success(
            self.request,
            f'Пост успешно изменен.'
        )
        return super().form_valid(form)
    
    
def load_posts(request):
    offset = int(request.GET.get('offset', 0))
    limit = 10  
    posts = Post.objects.all().order_by('created_at')[offset:offset + limit]
   
    posts_data = [
        {
            'title': post.title,
            'price': post.price,
            'created_at': post.created_at.strftime('%Y-%m-%d'),
            'created_time':post.created_at.strftime("%H:%M"),
            'block': post.block,
            'image_url': post.images.first().image.url if post.images.exists() else ''
        }
        for post in posts
    ]
    print("12345", posts_data)
    return JsonResponse({'posts': posts_data})