from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from apps.cart.cart import Cart
from .forms import AddToCartForm
from .models import Category, Product
from ..costumer.decorators import costumer_required
from ..costumer.models import Costumer
from ..order.utilities import send_notification


def search(request):
    query = request.GET.get('query', '')
    sel_category = request.GET.get('category', '')
    sel_ordering = request.GET.get('order', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(is_sold=False)
    if sel_category != "Select category":
        category = get_object_or_404(Category, title=sel_category)
        products = products.filter(category=category).filter(is_sold=False)
    else:
        sel_category = "All"
    ORDERING = {
        "date (new-old)": "-date_added",
        "date (old-new)": "date_added",
        "price (low-high)": "price",
        "price (high-low)": "-price",
    }
    ordering = ORDERING.get(sel_ordering, "")
    if ordering:
        products = products.order_by(ordering)
    else:
        sel_ordering = "Default"
    context = {'products': products, 'query': query, 'category': sel_category, 'order': sel_ordering}
    return render(request, 'product/search.html', context)


def product(request, category_slug, product_slug, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug, id=product_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The product has been added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug, product_id=product_id)
    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id).exclude(is_sold=True))

    # if len(similar_products) >= 4:
    #    similar_products = random.sample(similar_products, 4)

    related_products = product.related_products()
    # if len(related_products) > 4:
    #    related_products = random.sample(related_products, 4)

    context = {'form': form, 'product': product, 'similar_products': similar_products,
               'related_products': related_products}
    return render(request, 'product/product.html', context)


@login_required
@costumer_required
def save_unsaved_product(request):
    user = request.user
    if request.method == 'POST':
        sel_product = request.POST.get('product')
        product = Product.objects.get(id=sel_product)
        costumer = Costumer.objects.get(created_by=user)

        if costumer in product.saved_by.all():
            product.saved_by.remove(costumer)
            send_notification(sender=costumer, recipient=product.vendor, action="remove_save", product=product)
            messages.error(request, "The product has been removed from favorites successfully")
        else:
            product.saved_by.add(costumer)
            send_notification(sender=costumer, recipient=product.vendor, action="add_save", product=product)
            messages.success(request, 'The product has been added  to favorites successfully')
        product.save()

    return redirect('product', category_slug=product.category.slug, product_slug=product.slug, product_id=product.id)
