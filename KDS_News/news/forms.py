from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Comment
import datetime


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1970,datetime.date.today().year)))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','dob' ,'password1', 'password2', )

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
    class Meta:
        model = User
        fields = ('username', 'password1' )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('favourite_category',"user_pic")

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ('content',)