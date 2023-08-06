from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from django.db.models import Q
from .form import RoomForm

# Create your views here.
# rooms = [
#     {"id":1, "name": "lets learn Python"},
#     {"id":2, "name": "lets learn Java"},
#     {"id":3, "name": "lets learn C++"}

# ]


def LoginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username name or password does not exist")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def RegisterPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        # we gonna take the data from the UserCreationForm and store into form variable
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # we also want to login user in
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration")
    return render(request, "base/login_register.html", {"form": form})


def LogoutPage(request):
    logout(request)
    return redirect("home")


def home(request):
    # the q variable store the value passed in url
    # if the q does't have a value do nothing else do this
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topic = Topic.objects.all()
    # icontains are used to for if there is similer workd like for python py like that
    # in q value matched room display
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    roomcount = rooms.count()
    context = {"rooms": rooms, "topics": topic, "roomcount": roomcount}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # in room model the message child model set all
    room_message = room.message_set.all().order_by("-create")
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            # in room.html we use name inside the text form
            body=request.POST.get("body"),
        )
        # every room have unique id that why we are padding pk
        return redirect("room", pk=room.id)
    room.participants.add(request.user)
    Participants = room.participants.all()
    context = {
        "rooms": room,
        "room_message": room_message,
        "Participants": Participants,
    }
    return render(request, "base/room.html", context)


# if the user is logout ,and user try to create a room it will go to login page
@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        # we gonna pass all the posted data to form
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # thi form gonna prefilled with the RoomForm exiting data
    form = RoomForm(instance=room)

    context = {"form": form}
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("home")
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete_room.html", context)


@login_required(login_url="login")
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect("home")
    context = {
        'obj': message
    }
    return render(request, "base/delete_room.html",context)
    