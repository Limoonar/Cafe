from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, OTPForm
from .models import Users
from django.contrib.auth.hashers import check_password
import ghasedakpack
from numpy.random import randint

sms = ghasedakpack.Ghasedak("a26658f51d8f300e354cf8d137bca49aab329de737a80c80f507fb883b2ffeba")



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
                if password == user.Password:
                    global phone, random_code
                    random_code= randint(1000,9999)
                    phone= '0'+str(user.Phone_Number)
                    message = str(random_code)
                    receptor = "09143658166"
                    linenumber = "10008566"
                    sms = ghasedakpack.Ghasedak("7cfab86d60b9fc7621f8a572dbec81d2628cfc6a387a05d724bc406d7848251f")
                    sms.send({
                        'message': message,
                        'receptor': receptor,
                        'linenumber': linenumber
                    })

                    # Store necessary data in session
                    request.session['temp_username'] = user.Username
                    request.session['random_code'] = random_code

                    return redirect('otp_verify')  # Redirect to OTP verification page
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

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']  # Remove username from session
    return redirect('index')  # Redirect to main page after logout


def otp_verify_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == str(request.session.get('random_code')):
                # OTP is correct
                request.session['username']=request.session['temp_username']
                del request.session['temp_username']  # Remove username from session
                return redirect('index')  # Redirect to main page
            else:
                error = 'Invalid OTP'
        else:
            error = 'Invalid form submission'
    else:
        form = OTPForm()
        error = None

    return render(request, 'otp_verify.html', {'form': form, 'error': error})
