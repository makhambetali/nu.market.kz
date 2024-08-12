from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField("Название товара", max_length=25)
    content = models.TextField("Подробно о товаре")
    price = models.CharField("Стоимость товара", max_length=15)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} - {self.price}'
    
    