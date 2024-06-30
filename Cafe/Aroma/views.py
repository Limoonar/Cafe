from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login
from .forms import *
from .models import Users, Orders, Product
from django.contrib.auth.hashers import check_password
import ghasedakpack
from numpy.random import randint
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse

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

            # Admin check
            if username_or_email == "admin" and password == "admin":
                request.session['username'] = "admin"
                return redirect('adminpage')  # Redirect to admin page

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
                    request.session['username'] = user.Username
                    request.session['cart']= {}
                    return redirect('index')
                    # global phone, random_code
                    # random_code = randint(1000, 9999)
                    # phone = '0' + str(user.Phone_Number)
                    # message = str(random_code)
                    # receptor = phone
                    # linenumber = "10008566"
                    # #sms = ghasedakpack.Ghasedak("7cfab86d60b9fc7621f8a572dbec81d2628cfc6a387a05d724bc406d7848251f")
                    # #sms.send({'message': message,'receptor': receptor,'linenumber': linenumber})

                    # # Store necessary data in session
                    # request.session['temp_username'] = user.Username
                    # request.session['random_code'] = random_code

                    # return redirect('otp_verify')  # Redirect to OTP verification page
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


# ADMIN PAGES
#@login_required
def adminpage_view(request):
    if request.session.get('username') != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    return render(request, 'adminpage.html')


def add_products_view(request):
    if request.session.get('username') != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
 
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_products')  # Redirect back to the form after successful submission
    else:
        form = ProductForm()

    return render(request, 'Add_productss.html', {'form': form})

#@login_required
def inventory_management_view(request):
    if request.session.get('username') != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    if request.method == 'POST':
        return redirect ('inventory_update')
    if request.method == 'GET':
        storage = Storage.objects.order_by('-id').first()
        return render(request, 'inventory_management.html', {'storage': storage})


def inventory_update_view(request):   
    if request.method == 'POST':
        #storage = request.POST
        form = UpdateInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_management')
    else:
        form = UpdateInventoryForm()
    return render(request, 'update_inventory.html', {'form': form})


# CUSTOMER PAGES
def customerpage_view(request):
    #if request.session.get('username') == 'admin':
    #    return HttpResponseForbidden("You are not allowed to access this page.")
    return render(request, 'customerpage.html')




def purchase_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # Assume we get the username from a session or form input
            # For demonstration, let's assume it's from the session
            username = request.session.get('username_or_email')
            if not username:
                return HttpResponse('User is not logged in', status=401)

            try:
                # Fetch the user from your custom Users model
                user = Users.objects.get(Username=username)
                order.save()  # Save the order before adding Many-to-Many relations
                order.Username.add(user)  # Add the user to the Many-to-Many field
                order.save()  # Save again after adding relations

                return redirect('purchase_success')
            except Users.DoesNotExist:
                try:
                    user = Users.objects.get(Email=username)
                    order.save()  # Save the order before adding Many-to-Many relations
                    order.Username.add(user)  # Add the user to the Many-to-Many field
                    order.save()  # Save again after adding relations
                except:
                    return HttpResponse('User not found', status=404)
    else:
        form = OrderForm()

    return render(request, 'purchase.html', {'form': form})


# PRODUCTS
#def hotdrinks_view(request):
    #products = Product.objects.filter(Vertical="Hot Drink")
    #context = {'products':products}
    #return render(request, 'Hot_Drink.html', context)

# views.py


def products_page_view(request):
    vertical = request.GET.get('vertical', 'All')

    if vertical == 'All':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(Vertical=vertical)

    context = {
        'vertical': vertical,
        'products': products,
        'vertical_choices': Product.VERTICAL_CHOICES,
    }
    return render(request, 'products_page.html', context)

def products_page_view(request):
    vertical = request.GET.get('vertical', 'All')
    if vertical == 'All':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(Vertical=vertical)

    cart = request.session.get('cart', {})

    context = {
        'products': products,
        'vertical': vertical,
        'vertical_choices': Product.VERTICAL_CHOICES,
        'cart': cart
    }

    return render(request, 'products_page.html', context)
    
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    vertical = request.POST.get('vertical', 'All')  # Get the current category from the request

    cart = request.session.get('cart', {})

    # Update the quantity of the product in the cart
    cart[str(product_id)] = quantity

    # Save the updated cart back to the session
    request.session['cart'] = cart

    # Redirect to the products page with the current category
    return redirect(f'/products/?vertical={vertical}')


def cart_view(request):
    cart = request.session.get('cart', {})
    products_in_cart = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        products_in_cart.append({
            'product': product,
            'quantity': quantity,
            'total': product.Price * quantity
        })
        total_price += product.Price * quantity

    context = {
        'products_in_cart': products_in_cart,
        'total_price': total_price
    }
    
    return render(request, 'cart_page.html', context)


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            if str(product_id) in cart:
                del cart[str(product_id)]

        request.session['cart'] = cart

    return redirect('cart')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            del cart[str(product_id)]

        request.session['cart'] = cart

    return redirect('cart')

'''def update_pickup_type(request):
    if request.method == 'POST':
        pickup_type = request.POST.get('pickup_type', 'take_away')  # Default to take away if not specified
        request.session['pickup_type'] = pickup_type

    return redirect('cart')'''


def finalize_purchase(request):
    if request.method == 'POST':
        # Retrieve cart from session
        cart = request.session.get('cart', {})
        
        if not cart:
            return redirect('cart')  # Redirect to cart if it's empty
        
        # Retrieve the logged-in user from session
        username = request.session.get('username')
        if not username:
            return redirect('login')  # Redirect to login if not logged in

        user = get_object_or_404(Users, Username=username)
        
        # Calculate total purchase amount
        total_amount = 0
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            total_amount += product.Price * quantity

        # Get the selected order type
        order_type = int(request.POST.get('order_type', 1))  # Default to 'Take Away' if not provided

        # Create an order
        order = Orders.objects.create(Purchase_amount=total_amount, Type=order_type)
        order.Username.add(user)
        
        # Add products to the order
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            order.Products.add(product)
        
        # Clear the cart
        request.session['cart'] = {}

        return redirect('thank_you')

    return redirect('cart')