from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """ A view to return the shopping cart page """

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a selected quantity of an item to a users shopping cart"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity

        if cart[item_id] > 99:
            cart[item_id] = 99
            messages.success(request, f'Max quantity (99) of {product.name} added to your cart!')
        else:
            messages.success(request, f'{product.name} was updated in your cart!')

    else:
        cart[item_id] = quantity
        messages.success(request, f'{product.name} was added to your cart!')

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, item_id):
    """ Update the quantity of an item in the users shopping cart"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    cart[item_id] = quantity

    messages.success(request, f'{product.name} was updated in your cart!')
    request.session['cart'] = cart
    return redirect(redirect_url)


def remove_from_cart(request, item_id):
    """ Remove an item from the users shopping cart"""

    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})
    cart.pop(item_id)

    messages.info(request, f'{product.name} was removed from your cart!')
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
