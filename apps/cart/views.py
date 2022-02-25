from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect

from apps.order.utilities import checkout, send_notification
from .cart import Cart
from .forms import CheckoutForm
from ..costumer.decorators import costumer_required
from ..order.models import OrderItem


@login_required
@costumer_required
def cart_detail(request):
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            try:

                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                country = form.cleaned_data['country']
                town_city = form.cleaned_data['town_city']
                postcode = form.cleaned_data['postcode']
                address_line_1 = form.cleaned_data['address_line_1']
                address_line_2 = form.cleaned_data['address_line_2']

                order = checkout(request, name, surname, email, phone_number, country, town_city, postcode,
                                 address_line_1, address_line_2, cart.get_total_cost())

                for item in OrderItem.objects.filter(order=order).all():
                    send_notification(sender=item.costumer, recipient=item.vendor, action="new_order",
                                      product=item.product)
                messages.success(request, 'The order has been concluded successfully')
                cart.clear()

                cart.product_sold()
                return redirect('success')

            except Exception as e:
                print(e.args)
                messages.error(request, 'There was something wrong with the payment')
    else:

        form = CheckoutForm(initial=model_to_dict(user))

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')

    return render(request, 'cart/cart.html', {'form': form})


@login_required
@costumer_required
def success(request):
    return render(request, 'cart/success.html')
