from decimal import Decimal
from django.conf import settings
from urllib3 import proxy_from_url
from product.models import Product

class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * int(item['quantity'])
            yield item
        
    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())
    
    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': (str(product.price))}
        if override:
            self.cart[product_id]['quantity'] = int(str(quantity))
        else:
            self.cart[product_id]['quantity'] += int(str(quantity))
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
