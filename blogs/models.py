from django.db import models
from django.contrib.auth.models import User

#category table model
class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # return name when object is called
    def __str__(self):
        return self.name

#posts table model
class Post(models.Model):    
    title = models.CharField(max_length=200)
    body = models.TextField()
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_image = models.FileField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # return title when object is called
    def __str__(self):
        return self.title