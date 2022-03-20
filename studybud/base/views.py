# ===> 'Q' is going to allow us to add (and || or) in our search parameters
# import email
# from multiprocessing import context
from pydoc import describe
from unicodedata import name
from django.db.models import Q 
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# ===> UserCreationForm will be use to handle our user register form
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# ===> Django flash messages
from django.contrib import messages
# ===> restrictions of user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.






def loginPage(request):
    # will be specify for only login
    page = 'login'
    
    
    
    # ===> if you are already logged in and you type login url or anything relate to the content of the page, so far you are already authenticated you will be automatically redirect to the home page.
    # if you are authenticated you should be in the login page or form.
    
    if request.user.is_authenticated:
        return redirect('home')
    
    
    # =====> we are getting the user input from the frontend inside our form
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        # ===> we are checking if the user exist
        try:
            user = User.objects.get(email=email)
            # ===> if the user does not exist we want to throw an error messages.
        except:
            # ===> the messages will be passed into our templates
            messages.error(request, 'User does not exist')
            
        # ===> if the user exist, he or she will be authenticated
        user = authenticate(request, email=email, password=password)

        # ===> if the user is not None that means we got a user
        if user is not None:
            # the login will add that session in the database and inside our browser then the user will be officially logged in.
            login(request, user)
            # ===> once a user is logged in they will be redirected to the home page
            return redirect('home')
        # ===> if the user is not logged in
        else:
            messages.error(request, 'User OR Password does not exist')
        
    context = {'page':page}
    return render(request, 'base/login_register.html', context)





# ===> so that the user can be able to logout
def logoutUser(request):
    # ===> this will delete the token therefore ending the session
    # ==> logout() method
    logout(request)
    return redirect('home')



def registerPage(request):
    # page = 'register'
    form = MyUserCreationForm()
    
    if request.method == 'POST': 
        # ===> all the user credential will be passed here including the password
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # ===> we want to get the username as lower case
            user.username = user.username.lower()
            user.save()
            # ===> we want to log a user in and send them to the homepage
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form':form})



@login_required(login_url='login')
def home(request):
    # ===> 'q' will be whatever we pass inside the url.
    # ===> 'GET' get method
    # ===> 'get' get function
    # ===> we are getting 'q'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # ===> it will filter the topics during the filtering  using __icontains for capital and case sensitive
    # ===> 'Q' is going to allow us to add (and || or) in our search parameters
    # ===> you will be able to search by [topic, name and description]
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )
    
    # ===> '[0:5]' will give us the first five topics in this queryset
    topics = Topic.objects.all()[0:5]
    # ===> to count the numbers of rooms availablevate
    room_count = rooms.count()
    # ===> filtering down by the room name
    # ===> you will be able to see all the activities of a particular topic
    # ===> you will be able to see a partiular messages for a particular room or a topics
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms,
               'topics': topics,
               'room_count': room_count,
                'room_messages':room_messages
               }
    return render(request, 'base/home.html', context)



@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    # ===> we are getting all the comment or messages of the room.
    # ===> the models name is Message but we are writing it in small letters
    # _set.all() means it will give us the messages that are inside or related in the specific room particular room
    # ===> .order_by('-created') is use to filter to get the only recent messages which means the newswst will be first
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        
        # ===> once a participants is added in the request.post method before they are redirected
        # ===> add(request.user) the user will be added to the manytomanyfield
        room.participants.add(request.user)
        
        # we want the page to reload and be back on that page with the get request
        return redirect('room', pk=room.id)
    
    context = {'room':room, 'room_messages': room_messages, 'participants':participants, }
    return render(request, 'base/room.html', context)






# <========> User Profile <========>
@login_required(login_url='login')

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    '''
    
    # users = User.objects.all()
    # ===> all the messages that we have in a room will be rendered out
    # ===> a user will be able to see all their activities
    '''
    
    room_messages = user.message_set.all()
    room = user.room_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'room':room, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)









# ===> you can only create a room only if you are logged in
# ===> the unregistered user will not be allow to login in
# ===> and they will always be redirected to the login page
@login_required(login_url='login')
def createRoom(request):
    form  = RoomForm()
    # ===> we are getting all the topics and passing them into them templates
    topics = Topic.objects.all()
    if request.method == 'POST':
        # ===> we are getting the topic from the form so we are going to set the value
        topic_name = request.POST.get('topic')
        # ===> we are using a method called 'get or create' 
        # ===> what is going to happen is that get or create 'get_or_create()' will return an object and created, so if we pass in the topic name for name the value, so for example when we add python or javascript which is already created, so 'get_or_create()' is going to get the value of python and is going to return it inside of the topic object, automatically created will be false because python wasnt created we have already have it, assuming we added a new value like java, and we dont have any java in how database at this point, what that we happen is that created wiil be true, and it will simply create the object and if it cant find the it will create i. which means if it cant find java it will create it.
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # ===>
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
       
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)






@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # ===> the form will be prefilled with the room value
    form = RoomForm(instance=room)
    
    
      # ===> we are getting all the topics and passing them into them templates
    topics = Topic.objects.all()
    
    # ===> if you are not the owner of the account and you try to perform any action in another person Post you will get an error
    # only a user can update their own post
    if request.user != room.host:
        return HttpResponse('Your are not allowed here')
    if request.method == 'POST':
        
        topic_name = request.POST.get('topic')
        # ===> we are using a method called 'get or create' 
        # ===> what is going to happen is that get or create 'get_or_create()' will return an object and created, so if we pass in the topic name for name the value, so for example when we add python or javascript which is already created, so 'get_or_create()' is going to get the value of python and is going to return it inside of the topic object, automatically created will be false because python wasnt created we have already have it, assuming we added a new value like java, and we dont have any java in how database at this point, what that we happen is that created wiil be true, and it will simply create the object and if it cant find the it will create i. which means if it cant find java it will create it.
        # ===> we be able to update the name, topics and the descriptions <===
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
                
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)





        
@login_required(login_url='login')    
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here')
    
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})



# ===> this allow the host to delete the message
@login_required(login_url='login')    
def deleteMessage(request, pk):
    # ===> a user can only delete their own message
    message = Message.objects.get(id=pk)
    # ===> we are checking if the user is the message owner
    # ===> to check if they are the message owner
    if request.user != message.user:
        return HttpResponse('Your are not allowed here')
    
 
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})




    # =====> Updating user  <=====
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            
            '''
            # ===> when the user is updated it will return to them back to the same page for the current logged in user.
            '''
            
        return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})





# =====> Topics Page  <=====
@login_required(login_url='login')
def topicsPage(request):
    
    '''
    # ===> 'q' will be whatever we pass inside the url.
    # ===> 'GET' get method
    # ===> 'get' get function
    # ===> we are getting 'q'
    '''
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    '''
    
    # ===> if the user search the 'q' method they will be set to the topics page
    '''
    
    
    topics  = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})






'''
# =====> Topics Page  <=====
# ===> it will store all the informations for the activities on this website
'''

def activityPage(request):
    # ===> we are getting all the message
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
    