from pyexpat import model
from sqlite3 import Timestamp
from time import time
from django.db import models
import razorpay
from orders.models import Order

# Create your models here.

class RazorPayOrder(models.Model):
    order = models.OneToOneField(
        Order, related_name='razor_pay_order', on_delete=models.CASCADE
    )
    rp_id = models.CharField(max_length=50, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.rp_id

class Transaction(models.Model):
    order = models.ForeignKey(
        Order, related_name='transactions', on_delete=models.CASCADE
    )
    razor_pay_order = models.ForeignKey(
        RazorPayOrder, related_name='transactions', on_delete=models.CASCADE
    )
    payment_id = models.CharField(max_length=50)
    payment_sig = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.payment_id
