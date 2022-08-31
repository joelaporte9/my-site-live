from distutils.command.upload import upload
from django.db import models
import psycopg2

 
class Category(models.Model):    
    name = models.CharField(max_length=100, null=False, blank=False) 

    def __str__(self):
        return self.name

class Photo(models.Model):    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.image)

class createAlbum(models.Model):
    title = models.CharField(max_length=100, null=False, blank=True)

    def __str__(self):
        return str(self.title)







    
        

