from django.contrib import admin
from .models import Category, Item
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category)
admin.site.register(Item)