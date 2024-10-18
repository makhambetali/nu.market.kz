from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q


def str_to_int(string):
    return int(''.join(filter(str.isdigit, string)))

class AccessRestrictionMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверка на то, принадлежит ли объект текущему пользователю
        if self.object.creator != self.request.user:
            context = {
                'message': "You don't have permission for this action."
            }
            return render(request, 'general/permission.html', context)

        return super().get(request, *args, **kwargs)

class HomeMixin(ListView):
    model = Post
    template_name = 'app/home.html'
    context_object_name = 'posts'
    paginate_by = 3


class HomePageView(HomeMixin):
    def get_queryset(self):
        # Access the request.user in the method
        if self.request.user.is_authenticated:
            return Post.objects.order_by('-created_at').exclude(creator=self.request.user)
        else:
            return Post.objects.order_by('-created_at')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'today': timezone.now().date(),
            'posts_count': self.get_queryset().count(),
        })
        return context

class FilterHomePage(HomeMixin):
    def get_queryset(self):
        self.subcategories_list = self.request.GET.getlist("subcategory")
        self.categories_list = self.request.GET.getlist("category")
        self.conditions_list = self.request.GET.getlist("condition")
        self.search_query = self.request.GET.get('q')
        if self.request.user.is_authenticated:
            queryset = Post.objects.order_by('-created_at').exclude(creator=self.request.user)
        else:
            queryset =  Post.objects.order_by('-created_at')
        # queryset = Post.objects.exclude(creator = self.request.user)

        if self.categories_list or self.conditions_list:
            queryset = queryset.filter(
                Q(condition__in=self.conditions_list) & Q(category__name__in=self.categories_list))

        if self.search_query:
            queryset = queryset.filter(Q(title__icontains=self.search_query) | Q(content__icontains=self.search_query))

        self.queryset_count = queryset.count()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        context['posts_count'] = self.queryset_count
        context['conditions_chosen'] = self.conditions_list
        context['categories_chosen'] = self.categories_list
        context['search_query'] = self.search_query
        context['page_type'] = 'filter'
        context['redirected'] = self.request.GET.get('redirect')
        return context


class PostMixin(LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'app/create_or_edit_post.html'
    success_url = reverse_lazy('app:home-page')

    def form_valid(self, form):
        form_instance = form.save(commit=False)
        form_instance.creator = self.request.user
        print("qqqq", form_instance.category)
        form_instance.save()

        if self.action == 'edit':
            PostImage.objects.filter(post=form_instance).delete()

        images = self.request.FILES.getlist('files')
        for index, image in enumerate(images):
            PostImage.objects.create(
                image=image,
                post=form_instance,
                is_primary=bool(index == 0)
            )

        action_message = 'добавлен' if self.action == 'create' else 'изменен'
        messages.success(self.request, f'Пост успешно {action_message}.')

        return super().form_valid(form)

class CreatePost(PostMixin, CreateView):
    action = 'create'

class EditPost(PostMixin, UpdateView):
    action = 'edit'

class DeletePost(LoginRequiredMixin,AccessRestrictionMixin, DeleteView):
    model = Post
    template_name = 'app/delete_confirmation.html'
    success_url = reverse_lazy('app:home-page')

class DetailPageView(DetailView):
    model = Post
    template_name = "app/post_details.html"
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(category = self.get_object().category).exclude(slug = self.get_object().slug)

        return context

@login_required
def addToFav(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Retrieve the post instance by slug
    FavPosts.objects.create(post=post, creator=request.user)  # Use post instance here
    return JsonResponse('added', safe=False)

@login_required
def deleteFromFav(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Retrieve the post instance by slug
    fav = FavPosts.objects.filter(post=post, creator=request.user)  # Ensure you filter by creator to avoid deletion errors
    fav.delete()
    return JsonResponse('deleted', safe=False)

class MyPostsPageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'app/my_posts.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.filter(creator = self.request.user)

class FavPostsPageView(LoginRequiredMixin, ListView):
    model = FavPosts
    template_name = 'app/fav_posts.html'
    context_object_name = 'fav_posts'

    def get_queryset(self):
        return FavPosts.objects.filter(creator=self.request.user)

