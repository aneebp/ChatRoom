#serialize is user to convert models or object into json data/object
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
        class Meta:
            model = Room
            fields = '__all__'  