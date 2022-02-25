from django.conf import settings
from django.contrib.auth.decorators import login_required

from apps.costumer.decorators import costumer_required
from apps.product.models import Product


@login_required
@costumer_required
class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def product_sold(self):
        for p, v in self.cart.items():
            print(self.cart.items())
            product = Product.objects.get(pk=p)
            product.quantity -= v.get("quantity", 0)
            if product.quantity <= 0:
                product.is_sold = True
            product.save()

    def add(self, product_id, quantity, update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'id': product_id}

        if update_quantity:
            new_quantity = self.cart[product_id]['quantity'] + int(quantity)
            if new_quantity <= Product.objects.get(pk=product_id).quantity:
                self.cart[product_id]['quantity'] = new_quantity

            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product_id)

        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].price for item in self.cart.values())
