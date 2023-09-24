from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from .models import UserProfile, User, WishList
from .forms import UserProfileForm
from checkout.models import Order
from products.models import Product


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, pk=request.user.id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()
    reviews = user.reviews.all()
    wishlist = user.wishlist.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'reviews': reviews,
        'wishlist': wishlist
    }

    return render(request, template, context)


def order_history(request, order_number):
    """ Display a past order confirmation """

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def wishlist_product(request, product_id):
    """
    Add a product to a users wishlist or remove it if the product is
    already in the wishlist
    """

    user = get_object_or_404(User, pk=request.user.id)
    product = get_object_or_404(Product, pk=product_id)

    if WishList.objects.filter(user=user).filter(product=product).exists():
        WishList.objects.filter(user=user).filter(product=product).delete()
        messages.success(request, (f'{product.name} removed from wishlist!'))
    else:
        WishList.objects.create(product=product,
                                user=user,
                                )
        messages.success(request, (f'{product.name} added to wishlist!'))

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
