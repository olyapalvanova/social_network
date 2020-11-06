from django import forms
from django.core.exceptions import ValidationError

from apps.users.models import User
from apps.chats.models import Message


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'city', 'school',
                  'work', 'image', 'music', 'books', 'interests', 'status',
                  'is_private']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This email does not exist.')
        return email


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'channel']


class MessageFormFriend(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
