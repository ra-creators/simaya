from decimal import Decimal
from django.conf import settings
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

    def print_cart(self):
        print(self.cart)

    def add(self, product, price, size, metal, diamond, quantity=1, override=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': (str(price)), 
                                     'size': size,
                                     'metal': metal,
                                     'diamond': diamond}
        if override:
            self.cart[product_id]['quantity'] = int(str(quantity))
        else:
            self.cart[product_id]['quantity'] += int(str(quantity))
        self.save()
        

    def remove(self, product):
        try:
            product_id = str(product.id)
        except:
            product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def increase_count(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            self.cart[pid]['quantity'] += 1
            self.save()
            return True
        return False
    
    def decrease_count(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            self.cart[pid]['quantity'] -= 1
            if self.cart[pid]['quantity'] == 0:
                self.remove(product_id)
            else:
                self.save()
            return True
        return False
    
    def clear(self):
        # Clear session
        del self.session[settings.CART_SESSION_ID]
        