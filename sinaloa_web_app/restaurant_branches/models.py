from django.db import models

# Create your models here.
class RestaurantBranch(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='restaurant/images/', verbose_name='logotipo')
    description = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    google_link = models.TextField()
    def __str__(self):
        return f"{self.name}"
    