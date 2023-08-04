from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product


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
