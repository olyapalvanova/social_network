from django import forms
from django.core.exceptions import ValidationError

from apps.users.models import User


class UserForm(forms.Form):
    first_name = forms.CharField(label='Your name', max_length=50)
    last_name = forms.CharField(label='Your last name', max_length=50)
    birth_date = forms.DateField(required=False)
    city = forms.CharField(label='Your city', max_length=50,
                           required=False)
    education = forms.CharField(label='Your education', max_length=50,
                                required=False)
    job = forms.CharField(label='Your job', max_length=50,
                          required=False)


class UserInfoForm(forms.ModelForm):
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
