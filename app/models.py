from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from unidecode import unidecode
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    key = models.CharField(max_length=20, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Post(models.Model):
    product_choice = {
        "new": "Новый",
        "used": "Использованный"
    }
    block_choice = {
        "A1":"A1",
        "A2":"A2"
    }
    title = models.CharField("Название товара", max_length=25)
    content = models.TextField("Подробно о товаре")
    price = models.IntegerField("Стоимость товара")
    condition = models.CharField("Состояние товара", choices=product_choice, max_length=20)
    block = models.CharField("Блок", max_length=10, choices=block_choice)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.price}'

    def save(self, *args, **kwargs):
        if not self.slug:  # Сначала проверяем, не пуст ли slug, чтобы не перезаписывать его
            transliterated_title = unidecode(self.title)
            self.slug = slugify(f'{transliterated_title}-{get_random_string(length=4)}')
        super(Post, self).save(*args, **kwargs)
class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to='data_images/')
    is_primary = models.BooleanField(default=False)

class FavPosts(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='fav_posts')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=30)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    def __str__(self) -> str:
        return self.user.username
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()