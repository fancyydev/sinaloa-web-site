from django.db import models
from restaurant_branches.models import RestaurantBranch
    
# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=255)
    restaurant_branch = models.ForeignKey(RestaurantBranch, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}-{self.restaurant_branch}"
    
class Category(models.Model):
    CATEGORIES_TYPES = [
        ('fria', 'Fria'),
        ('caliente', 'Caliente'),
        ('postres', 'Postres'),
        ('bebidas', 'Bebidas'),
    ]
    name= models.CharField(max_length=255)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=CATEGORIES_TYPES)
    slug = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}-{self.menu}"

class Dishes(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    img = models.ImageField(upload_to='dishes/images/', verbose_name='platillo')
    price = models.DecimalField(max_digits=5,decimal_places=2)
    def __str__(self):
        return f"{self.name}-{self.category}-{self.price}" 
    
