from enum import auto
from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from user_manager.models import UserAddress
User = get_user_model()

STATUS_CHOICES = (
    ('Created', 'Created'),
    ('Picked Up', 'Picked Up'),
    ('Out For Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

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
        return float(self.discount) * float(self.get_total_cost())

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
    size = models.CharField(max_length=5)
    metal = models.CharField(max_length=10)
    diamond = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def sub_total(self):
        return self.get_cost()

    def get_cost(self):
        return self.price * self.quantity


# class OrderTracking(models.Model):
#     order = models.OneToOneField(Order, 
#                                  related_name='order_tracking',
#                                  on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.id)

class OrderTrackingStatus(models.Model):
    Order = models.ForeignKey(Order,
                              related_name='order_tracking_status',
                              on_delete=models.CASCADE)
    # order_tacking = models.ForeignKey(OrderTracking,
    #                                   related_name='order_tracking_status',
    #                                   on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.message:
            return f"{self.status} -  {self.message}"
        else:
            return f"{self.status}"

    @property
    def get_message(self):
        if self.message:
            return self.message
        else:
            return ""

    @property
    def get_location(self):
        if self.location:
            return self.location
        else:
            return ""

    @property
    def getDetails(self):
        return f"{self.status} - {self.get_location} {self.created} {self.get_message}"