from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, CustomUserCreationForm


# -----------------------LOGIN USER---------------------
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.ERROR(request, "Username or Password is invalid!!")

    context = {'page': page}
    return render(request, 'base/login-register.html', context)

# -----------------------LOGOUT USER---------------------
def logoutUser(request):
    logout(request)
    return redirect('home')

# -----------------------REGISTER USER---------------------
def registerUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error while sign up!!")

    context = {'form': form}
    return render(request, 'base/login-register.html', context)

# -----------------------USER PROFILE---------------------
def userProfile(request, pk):
    user = User.objects.get(id=pk)

    rooms = user.room_set.all()
    allMessages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'allMessages': allMessages, 'topics': topics}
    return render(request, 'base/profile.html', context)

# -----------------------HOME PAGE---------------------
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )


    topics = Topic.objects.all()
    allMessages = Message.objects.all()
    roomCount = Room.objects.all().count()

    context = {'rooms': rooms, 'topics': topics, 'allMessages': allMessages, 'roomCount': roomCount}
    return render(request, 'base/home.html', context)


# -----------------------SINGLE ROOM---------------------
def room(request, pk):
    room = Room.objects.get(id=pk)

    roomMessages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST['body']
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    
    context = {'room': room, 'roomMessages': roomMessages, 'participants': participants}
    return render(request, 'base/room.html', context)

# -----------------------CREATE A NEW ROOM---------------------
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST['room-topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST['name'],
            description = request.POST['description']
        )
        messages.success(request, "Room created successfully!!")
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/create-room.html', context)

# -----------------------UPDATE A ROOM---------------------
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        messages.error(request, "You are not allowed here!!")
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST['room-topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST['name']
        room.description = request.POST['description']
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/create-room.html', context)

# -----------------------DELETE A ROOM---------------------
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.error(request, "You are not allowed here!!")
        return redirect('home')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)

# -----------------------DELETE A MESSAGE---------------------
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.error(request, "You are not allowed here!!")
        return redirect('home')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)

    context = {'obj': message}
    return render(request, 'base/delete.html', context)

# -----------------------UPDATE USER PROFILE---------------------
@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update-profile.html', context)