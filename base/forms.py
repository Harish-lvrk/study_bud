from django.forms import ModelForm
from .models import Room, Profile
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta: # this is a class that is used to define the meta data of the form
        model = Room
        fields = '__all__' # this means all the fields in the model will be included in the form 
        exclude = ['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']