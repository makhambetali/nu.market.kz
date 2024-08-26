from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    room = models.CharField(max_length=50)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.message[:50]}"