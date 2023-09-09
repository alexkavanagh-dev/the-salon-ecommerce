from django.shortcuts import render
from products.models import Product

# Create your views here.


def index(request):
    """ A view to return the index page """

    products = Product.objects.all()

    feat_products = products.filter(brand__icontains='Olaplex')
    feat_products = feat_products[:4]

    context = {
        'feat_products': feat_products,
    }

    return render(request, 'home/index.html', context)
