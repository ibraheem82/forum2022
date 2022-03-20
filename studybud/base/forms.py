# from dataclasses import field
# from pyexpat import model
from dataclasses import field
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Room, User
# from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # ===> we wont select a user our self in order to post
        # ===> the person that owns the account will be prefilled so that he can post
        # ===> we wont see the host and the paticipants when creating a topic 
        # ===> only the user that is logged in will be able to create a topic
        exclude = ['host', 'paticipants']
        
        
        
# =====> Using a model form that will be passed to templates form the user to update their profile <=====
# ===> user will update username and email
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']