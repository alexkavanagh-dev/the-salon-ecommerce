from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Review, Category
from .forms import ReviewForm, ProductForm


def all_products(request):
    """ A view to show all products, including search queries with
        pagination
    """

    products = Product.objects.all()
    request_type = ""
    query = None
    categories = None
    sort = None
    direction = None

    if request.method == "GET":
        # Sorting
        if 'sort' in request.GET:

            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        # Search queries
        if 'q' in request.GET:
            request_type = "search"

            query = request.GET.get("q")

            if query.isspace():
                products = []

            else:
                products = products.filter(
                    Q(name__icontains=query)
                    | Q(brand__icontains=query)
                    | Q(description__icontains=query)
                    )

        # Categories
        if 'category' in request.GET:
            request_type = "category"

            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        current_sorting = f'{sort}_{direction}'
        page_number = request.GET.get("page")
        paginator = Paginator(products, 12)
        page_obj = paginator.get_page(page_number)
        template = "products/products.html"
        context = {
            "page_obj": page_obj,
            "request_type": request_type,
            "current_sorting": current_sorting,
            "current_category": categories
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


def add_product(request):
    """
    Take information/image from admin to create a new product
    """
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST, files=request.FILES)

        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.save()
            messages.success(request, 'New product was added successfully!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Please check that the form has been '
                                    'filled correctly.')
    else:
        product_form = ProductForm()

    return render(request, 'products/add_product.html', {"product_form": product_form})
