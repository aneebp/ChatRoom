from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm



class userCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']  


# modelform class take the room datamodel and create a form
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['avater','name','username','email','bio']       
    