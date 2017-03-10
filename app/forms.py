from django.contrib.auth.models import User
from django import forms

from .models import Topic

class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['title', 'content', 'requirement_for', 'main_requirement', 'is_basic', 'is_first']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
