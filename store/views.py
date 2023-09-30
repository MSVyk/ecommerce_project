from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import stripe
from django.conf import settings
from .forms import ProductForm  # Import the ProductForm created earlier
from .models import Product  # Import the Product model if not already imported
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib.auth.decorators import user_passes_test


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff_or_superuser)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.save()
        # You can add more logic like sending email notifications here
        return redirect('order_history')

    return render(request, 'templates/store/update_order_status.html', {'order': order})

@login_required(login_url='/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'templates/store/order_history.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'templates/registration/register.html', {'form': form})


# def register(request):
#     if request.method == "POST":
#         # Create a UserCreationForm instance with the POST data
#         form = UserCreationForm(request.POST)

#         # Check if the form is valid
#         if form.is_valid():
#             # Save the user, but don't commit to the database yet
#             user = form.save(commit=False)
#             # Get the cleaned username and password from the form
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password1")

#             # Set the user's password
#             user.set_password(password)

#             # Save the user with the updated password
#             user.save()

#             # Authenticate the user
#             user = authenticate(username=username, password=password)

#             # Log the user in
#             login(request, user)
#             # Redirect to a success page (e.g., "product_list")
#             return redirect("product_list")
#     else:
#         # For GET requests, create an empty UserCreationForm instance
#         form = UserCreationForm()

#     # Render the registration form template with the form context
#     return render(request, "registration/register.html", {"form": form})

@login_required(login_url='/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'templates/store/product_list.html', {'products': products})

@login_required(login_url='/login/')
def cart(request):  ## <==  TO BE CHNAGED
    products = Product.objects.all()
    return render(request, 'templates/store/cart.html', {'products': products})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'templates/registration/login.html', {'form': form})


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='/login/')
def checkout(request):
    if request.method == 'POST':
        # Handle the payment processing with Stripe
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=int(request.session['total_price'] * 100),  # Amount in cents
                currency='usd',
                description='Payment for Order',
                source=token,
            )
        except stripe.error.CardError as e:
            # Handle card payment error
            pass

        # Create an order in your database
        # Clear the cart
        request.session['cart'] = []

        return render(request, 'templates/store/payment_success.html')
    else:
        return render(request, 'templates/store/checkout.html')

@login_required(login_url='/login/')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list page after successful submission
    else:
        form = ProductForm()

    return render(request, 'templates/store/product_form.html', {'form': form})

def home(request):  ## <==  TO BE CHNAGED
    return render(request, 'templates/base.html')