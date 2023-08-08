from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Review
from .forms import ReviewForm


def all_products(request):
    """ A view to show all products with pagination """

    products = Product.objects.all()

    page_number = request.GET.get("page")
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)
    template = "products/products.html"
    context = {
        "page_obj": page_obj
    }
    return render(request, template, context)


def product_detail(request, product_id):
    """ A view to show a detailed product page """

    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.order_by('created_on')
    template = "products/product_detail.html"
    context = {
        "product": product,
        "reviews": reviews,
        "review_form": ReviewForm()
    }
    return render(request, template, context)
