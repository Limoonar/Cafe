from django import forms

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)