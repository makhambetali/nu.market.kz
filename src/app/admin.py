from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','price','condition', 'block','category','creator')
    prepopulated_fields = {"slug": ("title", "price")}

admin.site.register(Post, PostAdmin)
# admin.site.register(Category)
admin.site.register(Profile)
class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1  # Количество пустых форм для подкатегорий

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]  # Отображение подкатегорий прямо в категории

admin.site.register(Category, CategoryAdmin)
# Register your models here.
