from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm
from .models import Users
from django.contrib.auth.hashers import check_password



def index(request):
    # Your main page logic here
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['Password']

            # Check if the username or email exists in the Users model
            try:
                user = Users.objects.get(Username=username_or_email)
            except Users.DoesNotExist:
                try:
                    user = Users.objects.get(Email=username_or_email)
                except Users.DoesNotExist:
                    user = None

            # If user exists, check password
            if user:
                # Manually compare hashed password
                if password==user.Password:
                    # Password matches
                    request.session['username'] = user.Username  # Example using session
                    return redirect('index')  # Redirect to main page on successful login
                else:
                    error = 'Invalid credentials'
            else:
                error = 'User not found'

        else:
            error = 'Invalid form submission'
    else:
        form = LoginForm()
        error = None

    return render(request, 'login.html', {'form': form, 'error': error})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})