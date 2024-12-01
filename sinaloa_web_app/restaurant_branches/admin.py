from django.contrib import admin
from .models import *

@admin.register(RestaurantBranch)
class RestaurantBranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email']
    search_fields = ['name', 'description', 'phone_number', 'email']
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
