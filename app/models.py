from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    product_choice = {
        "new": "Новый",
        "used": "Использованный"
    }
    block_choise = {
        "A1":"A1",
        "A2":"A2"
    }
    title = models.CharField("Название товара", max_length=25)
    content = models.TextField("Подробно о товаре")
    price = models.CharField("Стоимость товара", max_length=9)
    condition = models.CharField("Состояние товара", choices=product_choice, max_length=20)
    block = models.CharField("Блок", max_length=10, choices=block_choise)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} - {self.price}'
    

class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to='data_images/')
    is_primary = models.BooleanField(default=False)