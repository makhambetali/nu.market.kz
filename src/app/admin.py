from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','price','condition', 'block','category','creator')
    prepopulated_fields = {"slug": ("title", "price")}

admin.site.register(Post, PostAdmin)
admin.site.register(Category)

