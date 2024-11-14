from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant_branch']
    search_fields = ['name', 'restaurant_branch']
    list_filter = ['restaurant_branch']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu']
    search_fields =  ['name', 'menu']
    list_filter = ['menu']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Dishes)
class DishesAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    search_fields = ['name', 'description', 'category', 'price']
    list_filter = ['category']