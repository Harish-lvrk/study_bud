from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta: # this is a class that is used to define the meta data of the form
        model = Room
        fields = '__all__' # this means all the fields in the model will be included in the form 
        