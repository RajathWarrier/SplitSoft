from typing import Tuple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as djUser

from . import models

def must_be_unique(value):
    user = djUser.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already Exists")
    return value

class AddGroupForm(forms.Form):
    users = models.User.objects.all()
    groupName = forms.CharField(
        label = "Group Name",
        required = True,
        max_length = 100
    )
    users = forms.MultipleChoiceField(
        # choices = [(user.id, (user.fName + " " + user.lName)) for user in models.User.objects.all()]
        label = 'Select Members (Including Youtself)',
        choices = [(user.id, (user.fName + " " + user.lName)) for user in users]
    )
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label = "First Name",
        required = True,
        max_length = 50
    )
    last_name = forms.CharField(
        label = "Last Name",
        required = False,
        max_length = 50
    )
    email = forms.EmailField(
        label = "Email",
        required = True,
        validators=[must_be_unique]
    )
    
    class Meta:
        model = djUser
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        app_user = models.User()
        app_user.acc_user = user
        app_user.fName = user.first_name
        app_user.lName = user.last_name
    
        if commit:
            user.save()
            app_user.save()
        return user
