from django.shortcuts import render, redirect
from .models import Room, Topic
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .froms import RoomForm
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

    q = request.GET.get('q') # this is used to get the data from the URL
    if q: # this checks if the get request is having any query parameter if having any 
      #  rooms = Room.objects.filter(topic__name__icontains=q, name__icontains=q) # this is used to filter the rooms by the topic name
        rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                  Q(name__icontains=q) |
                                  Q(description__icontains=q)) # this is used to filter the rooms by the topic name and the room name
    else:
        rooms = Room.objects.all()
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics, 'q':q, 'rooms_count':rooms_count}
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=int(pk))
    context = {'room':room}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_from.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=int(pk)) # this is used to get the data from the model
    form = RoomForm(instance=room) # this is used to get the data from the model and put it in the form
    if request.user != room.host:
        return HttpResponse('You are not authorized to update this room')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) # this is used to get the data from the model and put it in the form
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_from.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk)) # this is used to get the data from the model
    if request.user != room.host:
        return HttpResponse('You are not authorized to delete this room')
    if request.method == 'POST':
        room.delete() # this is used to delete the data from the model
        return redirect('home')
    context = {'room':room}
    return render(request, 'base/delete.html', context)

from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')

    return render(request, 'base/login_register.html')

def logoutUser(request):
    logout(request)
    return redirect('home')
