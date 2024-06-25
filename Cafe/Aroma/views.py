from django.shortcuts import render
from .models import Product

def index(request):
    # Your main page logic here
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to main page on successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
