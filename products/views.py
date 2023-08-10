from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Review
from .forms import ReviewForm


def all_products(request):
    """ A view to show all products, including search queries with
        pagination
    """

    products = Product.objects.all()

    if request.method == "GET":
        # Search queries
        if 'q' in request.GET:

            query = request.GET.get("q")

            if query.isspace():
                query_results = []

            else:
                query_results = products.filter(
                    Q(name__icontains=query)
                    | Q(brand__icontains=query)
                    | Q(description__icontains=query)
                    )

            page_number = request.GET.get("page")
            paginator = Paginator(query_results, 12)
            page_obj = paginator.get_page(page_number)
            template = "products/products.html"
            context = {
                "page_obj": page_obj
            }
            return render(request, template, context)

        # All products
        else:
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
