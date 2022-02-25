from django.contrib.auth.decorators import login_required
from notifications.signals import notify

from apps.cart.cart import Cart
from .models import Order, OrderItem
from ..costumer.decorators import costumer_required


@login_required
@costumer_required
def checkout(request, name, surname, email, phone_number, country, town_city, postcode,
             address_line_1, address_line_2, amount):
    order = Order.objects.create(name=name, surname=surname, email=email, country=country, town_city=town_city,
                                 postcode=postcode, address_line_1=address_line_1, address_line_2=address_line_2,
                                 phone_number=phone_number, paid_amount=amount, costumer=request.user.costumer,
                                 costumer_has_paid=True)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], vendor=item['product'].vendor,
                                 costumer=request.user.costumer,
                                 price=item['product'].price, quantity=item['quantity'])

        order.vendors.add(item['product'].vendor)
        order.save()
    return order


def send_notification(sender, recipient, action, product=None):
    messages = {
        "new_order": f"you have a new order of {product}",
        "remove_save": f"{sender} removed {product} from favorites",
        "add_save": f"{sender} added {product} to favorites",
        "confirm_delivery": f"{sender} confirmed the delivery for {product}",
        "leave_review": f"{sender} left you a review",
        "confirm_shipment": f"{sender} confirmed the shipment of {product}",

    }
    message = messages.get(action, "")

    receiver = recipient.created_by

    notify.send(actor=sender, sender=sender, recipient=receiver, verb='Message', description=message,
                action_object=product)
