from django import forms
from .models import Users, Product
from django.contrib.auth.hashers import make_password



class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=100)
    Password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['Username', 'Full_name', 'Email', 'Phone_Number', 'Password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('Password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return confirm_password

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        password = self.cleaned_data["Password"]
        user.Password = make_password(password)  # Hash the password
        if commit:
            user.save()
        return user

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['Name', 'Sugar', 'Coffee', 'Flour', 'Chocolate', 'Price', 'Vertical']