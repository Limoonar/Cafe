from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def index(request):
    pass


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to main page on successful login
            else:
                error = 'Invalid credentials'
        else:
            error = 'Invalid form submission'
    else:
        form = LoginForm()
        error = None

    return render(request, 'login.html', {'form': form, 'error': error})

def home(request):
    best_selling_products = Product.objects.order_by('-sales')[:12]  # Fetch top 12 best-selling products
    context = {
        'best_selling_products': best_selling_products,
    }
    return render(request, 'home.html', context)
