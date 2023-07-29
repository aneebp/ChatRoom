from django.shortcuts import render
from .models import Room

# Create your views here.
# rooms = [
#     {"id":1, "name": "lets learn Python"},
#     {"id":2, "name": "lets learn Java"},
#     {"id":3, "name": "lets learn C++"}

# ]


def home(request):
    rooms = Room.objects.all()
    return render(request , 'base/home.html',{'rooms':rooms})


def room(request,pk):
    rooms = Room.objects.get(id=pk)
    return render(request , 'base/room.html',{'rooms' : rooms})