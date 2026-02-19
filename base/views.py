from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm, UserForm
from django.db.models import Q # this is used to filter the rooms by the topic name



# Create your views here.



# rooms = [
#     {
#         'id':1,
#         'name':'Let\'s learn Python'
#     },
#     {
#         'id':2,
#         'name':'Let\'s learn Java'
#     },
#     {
#         'id':3,
#         'name':'Let\'s learn C++'
#     },
# ]



def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q))

    topics = Topic.objects.all()
    rooms_count = rooms.count()
    recent_messages = Message.objects.filter(Q(room__name__icontains=q) | 
                                                Q(room__topic__name__icontains=q))[:50]
    context = {'rooms':rooms, 'topics':topics, 'q':q, 'rooms_count':rooms_count, 'recent_messages':recent_messages}
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=int(pk))
    room_messages = room.message_set.all().order_by('-created') # this means getting the particular messages belogns to this room
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        ) 
        room.participants.add(request.user)  # this helps that when evver the user messages here that user is a participant of this room for this room
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')

        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not authorized to update this room')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'room': room, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk)) # this is used to get the data from the model
    if request.user != room.host:
        return HttpResponse('You are not authorized to delete this room')
    if request.method == 'POST':
        room.delete() # this is used to delete the data from the model
        return redirect('home')
    context = {'obj':room}
    return render(request, 'base/delete.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower() # this is used to get the data from the model and put it in the form 
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            pass  # form errors will display inline
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def deleteMessage(request, pk):
    room_message = Message.objects.get(id=int(pk)) # this is used to get the data from the model
    if request.user != room_message.user:
        return HttpResponse('You are not authorized to delete this message')
    
    if request.method == 'POST':
        room_message.delete() # this is used to delete the data from the model
        return redirect('room', pk=room_message.room.id)
    context = {'obj':room_message}
    return render(request, 'base/delete.html', context)
    

def userProfile(request, pk):
    user = User.objects.get(id=int(pk))
    rooms = user.room_set.all()
    recent_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'recent_messages':recent_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        # this is used to update the data from the model 
        user = request.user
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('user-profile', pk=user.id)
    context = {'form':form}
    return render(request, 'base/update_profile.html', context)
