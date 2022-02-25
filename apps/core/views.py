from django.shortcuts import render

from apps.product.models import Product


def frontpage(request):
    newest_products = Product.objects.filter(is_sold=False).order_by('-date_added')[0:8]

    return render(request, 'core/frontpage.html', {'newest_products': newest_products})


def contact(request):
    return render(request, 'core/contact.html')
