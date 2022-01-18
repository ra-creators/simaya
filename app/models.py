from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here

CATEGORY_CHOICES=(
    ('Ring','Ring'),
    ('Earring','Earring'),
    ('Bracelet','Bracelet'),
    ('Necklace','Neclace')
)

class Product(models.Model):
    titel=models.CharField(max_length=100)
    selling_price=models.PositiveIntegerField()
    discounted_price=models.PositiveIntegerField()
    discription=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=10)
    product_image=models.ImageField(upload_to='productimg')

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)