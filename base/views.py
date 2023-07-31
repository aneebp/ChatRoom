from django.shortcuts import render,redirect
from .models import Room
from .form import RoomForm

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


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        #we gonna pass all the posted data to form
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request , 'base/room_form.html',context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    #thi form gonna prefilled with the RoomForm exiting data
    form = RoomForm(instance=room)
    context = {'form':form}
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request , 'base/room_form.html',context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj' : room}
    return render(request , 'base/delete_room.html',context)
    
