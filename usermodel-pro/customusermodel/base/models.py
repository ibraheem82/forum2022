from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
'''
# ===> we are building our own user model so that it inherit from the orginal django user models, then we extend it.
'''
# ===> [User] is inheriting from the AbstractUser
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    # ===> [(unique=True)] means two users cant have same email
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    
    # ===> [USERNAME_FIELD = 'email'] means the username field in the admin panel is now set to email field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []