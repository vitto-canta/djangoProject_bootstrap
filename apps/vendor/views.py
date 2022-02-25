from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.text import slugify

from apps.vendor.models import Vendor
from .decorators import vendor_required
from .forms import ProductForm
from ..order.models import OrderItem
from ..order.utilities import send_notification


@login_required
@vendor_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.filter(is_sold=False)
    reviews = vendor.reviews.all()
    orders = vendor.sellers.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html',
                  {'vendor': vendor, 'products': products, 'orders': orders, 'reviews': reviews})


@login_required
@vendor_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            messages.success(request, 'The product has been added successfully')
            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {'form': form})


@login_required
@vendor_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')

        if name:
            vendor.name = name
            vendor.save()
            messages.success(request, 'Your vendor name has been changed')
            return redirect('vendor_admin')

    return render(request, 'vendor/edit_vendor.html', {'vendor': vendor})


@login_required
@vendor_required
def recover_credit(request):
    vendor = request.user.vendor
    orders = vendor.sellers.all()
    if vendor.get_not_paid_amount() > 0:
        for order in orders:
            for item in order.items.all():
                if item.vendor == vendor:
                    item.vendor_paid = True
                    item.save()
        messages.success(request, 'The credit has been recovered successfully')

    else:
        messages.error(request, "you don't have any credit to recover")
    return redirect("vendor_admin")


@login_required
@vendor_required
def confirm_shipment(request, pk):
    item = OrderItem.objects.get(pk=pk)

    item.is_shipped = True
    item.save()
    send_notification(sender=request.user, recipient=item.costumer, action="confirm_shipment", product=item.product)

    return redirect("vendor_admin")


def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendors': vendors})


def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    reviews = vendor.reviews.all()

    return render(request, 'vendor/vendor.html', {'vendor': vendor, 'reviews': reviews})
