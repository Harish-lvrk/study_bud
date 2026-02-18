from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # on_delete=models.SET_NULL means if the topic is deleted, the room will not be deleted, bull = true means
    # participants  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200) # max_length=200 means it will store the maximum of 200 characters
    description = models.TextField(null=True, blank=True) # null for the database and blank which means it can be empty for the forms and also it will not throw an error if the field is empty
    updated = models.DateTimeField(auto_now=True) # auto_now=True means it will update the time every time the model is saved
    created = models.DateTimeField(auto_now_add=True) # auto_now_add=True means it will add the time only once when the model is created
    
    class Meta:
        ordering = ['-updated', '-created'] # this means the rooms will be ordered by the updated time and then by the created time in descending order

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # on_delete=models.CASCADE means if the user is deleted, the message will also be deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # on_delete=models.CASCADE means if the room is deleted, the message will also be deleted
    body = models.TextField() # body is the message itself
    updated = models.DateTimeField(auto_now=True) # auto_now=True means it will update the time every time the model is saved
    created = models.DateTimeField(auto_now_add=True) # auto_now_add=True means it will add the time only once when the model is created
    
    def __str__(self):
        return self.body[:50]


