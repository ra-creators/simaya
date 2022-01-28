from enum import auto
from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from user_manager.models import UserAddress
User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        User, related_name='order_details', on_delete=models.CASCADE)
    address = models.ForeignKey(
        UserAddress, related_name='order_details', on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(default='nil', max_length=100)
    razorpay_invoice_id = models.CharField(default='nil', max_length=100)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def name(self):
        return self.__str__()

    @property
    def total(self):
        return float(self.get_total_cost()) - float(self.discount_amount)

    @property
    def discount_amount(self):
        pass

    def save(self, *args, **kwargs):
        # for order_item in self.items.all():
        #     try:
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def sub_total(self):
        return self.get_cost()

    def get_cost(self):
        return self.price * self.quantity