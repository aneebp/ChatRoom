from django.forms import ModelForm
from .models import Room

# modelform class take the room datamodel and create a form
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']
    