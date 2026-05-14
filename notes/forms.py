from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Group, Note, Subgroup


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class GroupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Group
        fields = ("name", "password")


class GroupPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class SubgroupForm(forms.ModelForm):
    class Meta:
        model = Subgroup
        fields = ("name",)


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "file")