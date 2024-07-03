from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login
from .forms import *
from .models import Users, Orders, Product
from django.contrib.auth.hashers import check_password
import ghasedakpack
from numpy.random import randint
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone

sms = ghasedakpack.Ghasedak("a26658f51d8f300e354cf8d137bca49aab329de737a80c80f507fb883b2ffeba")



def index(request):
    # Query to get the top 2 most ordered products
    top_products = Product.objects.annotate(num_orders=Count('Orders')).order_by('-num_orders')[:2]

    context = {
        'top_products': top_products,
    }
    return render(request, 'index.html', context)

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


'''def products_page_view(request):
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
    return render(request, 'products_page.html', context)'''

def products_page_view(request):
    if request.session.get('username') == 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    else:
        vertical = request.GET.get('vertical', 'All')
        if vertical == 'All':
            products = Product.objects.all()
        else:
            products = Product.objects.filter(Vertical=vertical)

        try:
            storage = Storage.objects.latest('id')
        except Storage.DoesNotExist:
            storage = None

        sold_out_products = []
        for product in products:
            if (storage and (storage.sugar < product.Sugar or
                             storage.flour < product.Flour or
                             storage.coffee < product.Coffee or
                             storage.chocolate < product.Chocolate)):
                product.is_sold_out = True
                sold_out_products.append(product.Name)
            else:
                product.is_sold_out = False
            product.available_quantity = calculate_available_quantity(product, storage)

        if sold_out_products:
            messages.warning(request, f"The following products are sold out: {', '.join(sold_out_products)}")

        return render(request, 'products_page.html', {
            'products': products,
            'vertical': vertical,
            'vertical_choices': Product.VERTICAL_CHOICES,
            'storage': storage
        })

def calculate_available_quantity(product, storage):
    available_sugar = storage.sugar // product.Sugar if product.Sugar else float('inf')
    available_coffee = storage.coffee // product.Coffee if product.Coffee else float('inf')
    available_flour = storage.flour // product.Flour if product.Flour else float('inf')
    available_chocolate = storage.chocolate // product.Chocolate if product.Chocolate else float('inf')

    return min(available_sugar, available_coffee, available_flour, available_chocolate)
    
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    vertical = request.POST.get('vertical', 'All')

    cart = request.session.get('cart', {})
    storage = Storage.objects.latest('id')

    if (storage.sugar >= product.Sugar * quantity and
        storage.flour >= product.Flour * quantity and
        storage.coffee >= product.Coffee * quantity and
        storage.chocolate >= product.Chocolate * quantity):

        if str(product_id) in cart:
            previous_quantity = cart[str(product_id)]
            storage.revert_inventory(product, previous_quantity)

        cart[str(product_id)] = quantity
        storage.update_inventory(product, quantity)
        storage.save()

        request.session['cart'] = cart
        messages.success(request, f"Added {product.Name} to the cart.")
    else:
        messages.error(request, f"Insufficient ingredients to add {product.Name} to the cart.")

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
        new_quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        if str(product_id) in cart:
            current_quantity = cart[str(product_id)]
            storage = Storage.objects.latest('id')

            storage.revert_inventory(product, current_quantity)
            storage.save()

            if (storage.sugar >= product.Sugar * new_quantity and
                storage.flour >= product.Flour * new_quantity and
                storage.coffee >= product.Coffee * new_quantity and
                storage.chocolate >= product.Chocolate * new_quantity):

                cart[str(product_id)] = new_quantity
                storage.update_inventory(product, new_quantity)
                storage.save()

                messages.success(request, f"Updated {product.Name} quantity to {new_quantity}.")
            else:
                storage.update_inventory(product, current_quantity)
                storage.save()
                messages.error(request, f"Insufficient ingredients to update {product.Name} quantity to {new_quantity}.")

        request.session['cart'] = cart

    return redirect('cart')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            product = get_object_or_404(Product, id=product_id)
            quantity = cart[str(product_id)]

            storage = Storage.objects.latest('id')
            storage.revert_inventory(product, quantity)
            storage.save()

            del cart[str(product_id)]
            messages.success(request, f"Removed {product.Name} from the cart.")

        request.session['cart'] = cart

    return redirect('cart')



def finalize_purchase(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        username = request.session.get('username')
        if not username:
            messages.error(request, "You must be logged in to complete the purchase.")
            return redirect('login')

        user = get_object_or_404(Users, Username=username)
        total_amount = 0
        storage = Storage.objects.latest('id')

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            if (storage.sugar < product.Sugar * quantity or
                storage.flour < product.Flour * quantity or
                storage.coffee < product.Coffee * quantity or
                storage.chocolate < product.Chocolate * quantity):
                messages.error(request, f"Insufficient ingredients for {product.Name}. Please adjust your cart.")
                return redirect('cart')
            total_amount += product.Price * quantity

        order_type = int(request.POST.get('order_type', 1))
        order = Orders.objects.create(Purchase_amount=total_amount, Type=order_type)
        order.Username.add(user)

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            order.Products.add(product)

        request.session['cart'] = {}
        messages.success(request, "Purchase finalized successfully!")
        return redirect('thank_you')

    return redirect('cart')


def order_history(request):
    username = request.session.get('username')
    orders = Orders.objects.filter(Username=username).prefetch_related('Products')
    context = {
        'orders': orders
    }
    return render(request, 'order_history.html', context)


def filter_orders(request):
    vertical = request.GET.get('vertical', 'all')

    if vertical == 'all':
        orders = Orders.objects.values('Products__Vertical', 'created_at__date').annotate(
            total_products=Count('Products'))
    else:
        orders = Orders.objects.filter(Products__Vertical=vertical).values('created_at__date').annotate(
            total_products=Count('Products'))

    data = list(orders)
    return JsonResponse(data, safe=False)
def adminpage_view(request):
    if request.session.get('username') != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    # Get all orders
    orders = Orders.objects.all()

    # Get the total number of products ordered each day
    order_data = orders.values('created_at__date').annotate(total_products=Count('Products'))

    # Get product verticals
    distinct_verticals = list(Product.objects.values('Vertical').distinct())

    context = {
        'order_data': order_data,
        'verticals': distinct_verticals,
    }

    return render(request, 'adminpage.html')


def best_selling_products_api(request):
    # Fetch the top 2 products based on the number of orders
    best_selling_products = Product.objects.annotate(num_orders=Count('Orders')).order_by('-num_orders')[:2]

    # Prepare JSON response
    data = {
        'products': [
            {
                'name': Product.Name,
                'price': Product.Price,
                'image_url': Product.image_url,
            }
            for product in best_selling_products
        ]
    }

    return JsonResponse(data)