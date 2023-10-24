from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from products.models import Product
from home.models import FAQ
from .forms import FAQForm

# Create your views here.


def index(request):
    """ A view to return the index page """

    products = Product.objects.all()

    feat_products = products.filter(brand__icontains='Olaplex')
    feat_products = feat_products[:4]

    cf_products = products.filter(cruelty_free=True).order_by('?')
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


def add_FAQ(request):
    """ A view to add a new question and answer to the FAQ model """

    if request.user.is_superuser:
        if request.method == 'POST':
            FAQ_form = FAQForm(data=request.POST)

            if FAQ_form.is_valid():
                new_FAQ = FAQ_form.save(commit=False)
                new_FAQ.save()
                messages.success(request, 'New FAQ added successfully!')
                return redirect(reverse('add_FAQ'))
            else:
                messages.error(request, 'Please check that the form has been '
                                        'filled correctly.')
        else:
            FAQ_form = FAQForm()

        return render(request, 'home/add_FAQ.html', {"FAQ_form": FAQ_form})
    else:
        messages.error(request, 'Sorry, you do not have permission to perform '
                                'that action.')
        return redirect(reverse('home'))


def privacy_policy(request):
    """ A view to show the websites privacy policy """

    return render(request, 'home/privacy.html')
