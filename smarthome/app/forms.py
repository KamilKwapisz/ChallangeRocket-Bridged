from django.contrib.auth.forms import User
from django.forms import ModelForm, PasswordInput, CharField
from .models import Comment


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput)
    password_confirm = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
