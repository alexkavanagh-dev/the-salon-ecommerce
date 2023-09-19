from django.shortcuts import render
from products.models import Product
from home.models import FAQ

# Create your views here.


def index(request):
    """ A view to return the index page """

    products = Product.objects.all()

    feat_products = products.filter(brand__icontains='Olaplex')
    feat_products = feat_products[:4]

    cf_products = products.filter(cruelty_free=True)
    cf_products = cf_products[:4]

    context = {
        'feat_products': feat_products,
        'cf_products': cf_products,
    }

    return render(request, 'home/index.html', context)


def frequently_asked_questions(request):
    """ A view to show questions/answers from the FAQ model """

    questions = FAQ.objects.all()

    context = {
        'questions': questions,
    }

    return render(request, 'home/FAQ.html', context)
