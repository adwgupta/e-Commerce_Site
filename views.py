# views.py
from .models import Product
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the home page after successful login
            return redirect('home')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


# views.py


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product_list.html', {'page_obj': page_obj})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# views.py


@login_required
def add_shipping_info(request):
    if request.method == 'POST':
        shipping_address = request.POST['shipping_address']
        customer = request.user.customer
        customer.shipping_address = shipping_address
        customer.save()
        # Redirect to the checkout page after adding shipping information
        return redirect('checkout')

    return render(request, 'add_shipping_info.html')

# views.py


@login_required
def checkout(request):
    if request.method == 'POST':
        # Handle the checkout process, such as calculating the total price, creating an order, etc.
        # ...
        # Redirect to the order confirmation page after successful checkout
        return redirect('order_confirmation')

    return render(request, 'checkout.html')


@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'view_order.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer)
    return render(request, 'order_history.html', {'orders': orders})

# views.py


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.customer.wishlist.add(product)
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.customer.wishlist.remove(product)
    return redirect('wishlist')
