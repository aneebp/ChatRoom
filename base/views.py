from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message ,User 
from django.db.models import Q
from .form import RoomForm,UserForm ,userCreation
# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str,force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



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
    form = userCreation()
    if request.method == "POST":
        form = userCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            email = form.cleaned_data.get('email') 
            user.save()
            
            # Email registration
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "base/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.info(
                request,
                "Thank you for registering. A verification email has been sent to your inbox. Please check your email to activate your account.",
            )
            return redirect("register")
        
        else:
            messages.error(request, "An error occurred during registration.")
    
    return render(request, "base/login_register.html", {"form": form})

def Activate(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Activate the user
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account has been activated.")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link.")
        return redirect("register")

def LogoutPage(request):
    logout(request)
    return redirect("home")


def home(request):
    # the q variable store the value passed in url
    # if the q does't have a value do nothing else do this
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topic = Topic.objects.all()[0:4]
    # icontains are used to for if there is similer workd like for python py like that
    # in q value matched room display
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    roomcount = rooms.count()
    home_message = Message.objects.filter(Q(
        room__topic__name__icontains=q
    ))
    context = {"rooms": rooms, "topics": topic, "roomcount": roomcount,"home_message":home_message}
    return render(request, "base/home.html", context)

login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    # we can get all the child of an object by using _set
    room_message = room.message_set.all()
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

@login_required(login_url="login")
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    home_message = user.message_set.all()
    context = {
        'user':user,
        'topics': topics,
        'rooms': rooms,
        'home_message': home_message,
    }
    return render(request , 'base/user_profile.html',context)

# if the user is logout ,and user try to create a room it will go to login page
@login_required(login_url="login")
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == "POST":
           topic_name = request.POST.get('topic')
           #if the topic is there is gonna go with that other wise it will create 
           topic,created = Topic.objects.get_or_create(name=topic_name)
           Room.objects.create(
               host = request.user,
               topic = topic,
               name = request.POST.get('name'),
               description = request.POST.get('description')
           )
           return redirect("home")
    context = {"form": form,"topics":topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # thi form gonna prefilled with the RoomForm exiting data
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    context = {"form": form,"topics":topics,'rooms':room}
    if request.method == "POST":
         topic_name = request.POST.get('topic')
           #if the topic is there is gonna go with that other wise it will create 
         topic,created = Topic.objects.get_or_create(name=topic_name)
         room.name = request.POST.get('name')
         room.topic = topic
         room.description = request.POST.get('description')
         room.save()
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
            return redirect('room' ,pk=message.room.id)
            

        context = {
            'obj': message
        }
        return render(request, "base/delete_room.html",context)
        

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        #REQUEST.FILES IS USER FOR AVATAR
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request,'base/update_user.html',{'form':form})

def topicView(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics":topics}
    return render(request,'base/topics.html',context)

@login_required(login_url="login")
def activityView(request):
    messages = Message.objects.all()
    context = {"messages":messages}
    return render(request,'base/activity.html',context)