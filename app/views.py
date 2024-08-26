from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.forms import BaseModelForm
from app.models import *
from app.forms import *
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Max,Min,Q
def str_to_int(string):
    return int(''.join(filter(str.isdigit, string)))


class HomePageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dist/home.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = Post.objects.all()
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if category:
            queryset = queryset.filter(category=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        self.min_dot = queryset.aggregate(Min("price"))['price__min']
        self.max_dot = queryset.aggregate(Max("price"))['price__max']

        previous_category = self.request.GET.get('previous_category')
        previous_condition = self.request.GET.get('previous_condition')
        # Если категория изменилась, сбрасываем min_price и max_price
        if (category and category != previous_category) or (condition and condition != previous_condition):
            self.min_price = self.min_dot
            self.max_price = self.max_dot
        else:
            self.min_price = self.request.GET.get('min_price', self.min_dot)
            self.max_price = self.request.GET.get('max_price', self.max_dot)

        # Применяем фильтрацию по цене
        if self.min_price and self.min_price != self.min_dot:
            queryset = queryset.filter(price__gte=self.min_price)
        if self.max_price and self.max_price != self.max_dot:
            queryset = queryset.filter(price__lte=self.max_price)

        self.queryset_count = queryset.count()
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        context['category'] = self.request.GET.get('category')
        context['condition'] = self.request.GET.get('condition')
        context['posts_count'] = self.queryset_count
        context['min_price'] = self.min_price
        context['max_price'] = self.max_price
        context['min_dot'] = self.min_dot
        context['max_dot'] = self.max_dot
        context['categories'] = Category.objects.all()
        context['previous_category'] = context['category']
        context['previous_condition'] = context['condition']
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'dist/post.html'
    success_url = reverse_lazy('app:home-page')
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            
            form.creator = request.user
            price = request.POST.get('price')
            form.price = str_to_int(price)
            
       
            form.save()
            images = self.request.FILES.getlist('files')
            for index in range(len(images)):
                PostImage.objects.create(image = images[index], post = form, is_primary = bool(index==0) )
            messages.success(
                self.request,
                f'Пост успешно добавлен.'
            )
            return redirect('app:home-page')
        else:
            print('error')
            return JsonResponse('error')
             
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
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['page'] = 'edit'
        return context
    
    
def load_posts(request):

    offset = int(request.GET.get('offset', 0))
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    print(category, '1232132')
    queryset = Post.objects.all()
    print(condition, '123')
    limit = 10  
    if category:
            # print('hello')
            queryset = queryset.filter(category=category)
    else: queryset = queryset.all()
    if condition:
            queryset = queryset.filter(condition=condition)
    if min_price:
            queryset = queryset.filter(price__gte=int(min_price))
    if max_price:
            queryset = queryset.filter(price__lte=int(max_price))
    # posts = Post.objects.filter(category = category).order_by('-created_at')[offset:offset + limit]
    posts = queryset.order_by('created_at')[offset:offset+limit]
   
    posts_data = [
        {
            'id':post.id,
            'title': post.title,
            'price': post.price,
            'created_at': post.created_at.strftime('%Y-%m-%d'),
            'created_time':post.created_at.strftime("%H:%M"),
            'block': post.block,
            'liked':FavPosts.objects.filter(post_id = post.id, creator = request.user).exists(),
            'image_url': post.images.first().image.url if post.images.exists() else ''
        }
        for post in posts
    ]
    return JsonResponse({'posts': posts_data})

class DetailPageView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "dist/details.html"
    context_object_name = 'post'


def addToFav(request, pk):

    FavPosts.objects.create(post_id=pk, creator = request.user)
    return JsonResponse('added',safe=False)

def deleteFromFav(request, pk):
    fav = FavPosts.objects.filter(post_id = pk)
    fav.delete()
    return JsonResponse('deleted', safe=False)


class FavPostsPageView(LoginRequiredMixin, ListView):
    model = FavPosts
    template_name = 'dist/liked.html'
    context_object_name = 'fav_posts'
    def get_queryset(self):
        return FavPosts.objects.filter(creator = self.request.user)
    
def delete(request):
    Post.objects.all().delete()
    return redirect('/')


class ProfilePageView(TemplateView):
    template_name = 'dist/profile.html'
    form_class = ProfileForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_image'] = ProfileForm()  # Добавьте форму в контекст
        
        return context
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid(): 
            profile_image = form.cleaned_data['image']

            # Получаем профиль пользователя
            profile, created = Profile.objects.update_or_create(
                user=self.request.user,  
                defaults={'image': profile_image}
            )
            return redirect('app:profile-page')
        else:
            context = self.get_context_data()
            context['form_image'] = form
            return render(request, self.template_name, context)
def update_user_data(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    exists = User.objects.filter(Q(username = username)|Q(email = email)).exclude(id = request.user.id).exists()
    if not exists:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        image = request.POST.get('profile_pic')
        User.objects.filter(id = request.user.id).update(username = username, email = email, first_name = first_name, last_name = last_name)
        Profile.objects.filter(user = request.user).update(contact = phone)
        messages.success(
            request,
            f'Данные пользователя успешно обновлены.'
        )
    else:
        messages.error(
                request,
                f'Пользователь с таким логином или почтой уже существует.'
            )
        #   return HttpResponse([first_name, last_name, email, phone, old_password, new_password, image])
    return redirect('app:profile-page')