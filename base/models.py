from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(null=True,unique=True)
    bio = models.TextField(null=True)

    avater = models.ImageField(null=True,default='avatar.svg')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    # topic have many room but room can have one topic
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    #the reason we use related_name is in host we already used User
    participants = models.ManyToManyField(User, related_name="participants")
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update','-create']

    def __str__(self):
        return self.name
    
    

class Message(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room , on_delete=models.CASCADE) 
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-update','-create']

    def __str__(self):
        return self.body[0:50]
    

