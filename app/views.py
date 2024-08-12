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

def str_to_int(string):
    return int(''.join(filter(str.isdigit, string)))
# Create your views here.
@login_required
def homePage(request):
    # return HttpResponse(f'Hello {request.user}!')
    return render(request, 'dist/index.html')

class HomePageView(LoginRequiredMixin, ListView):
    model = Post

    template_name = 'dist/home.html'
    context_object_name = 'posts'


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'dist/create-post.html'
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
    template_name = 'dist/create-post.html'
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
    
    
