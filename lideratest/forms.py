from django.forms import ModelForm
from .models import Clase, Task
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class Taskform(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description', 'important', 'assigned_to']


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
   
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        
class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre', 'descripcion']

