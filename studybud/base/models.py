# from pyexpat import model
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


'''
===> we are not longer using this user model that django gave us.
# from django.contrib.auth.models import User
'''


# Create your models here.


# ===> we want django to look at our new user models
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    
    
    # ===> this default image will show when the user register inside the website
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []







class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name



class Room(models.Model):
    # ===> someone has to host the room
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # ===> if a topic is deleted, we dont want to delete the room that why we are setting it to on_delete=models.SET_NULL, null=True
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # ===> nulll is for the database  while blank is for the save method
    description = models.TextField(null=True, blank=True)
    # ===> stores the active users in a room
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # ===> the newest post will come to the top
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    
    
    
    # ========> Room Messages <========
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # ===> the newest post will come to the top
        ordering = ['-updated', '-created']
    # ===> will give us the first 50 characters of the message
    def __str__(self):
        return self.body[0:50]
