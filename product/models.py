from pydoc import describe
from unicodedata import category
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

GENDER_CHOICES = (
    ("Man", 'Man'),
    ('Woman', 'Woman')
)

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    thumbnail = models.ImageField(
        upload_to='categories/%Y/%m/%d', blank=True,
        default='defaults/categories_no_img.png'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return '/media/defaults/categories_no_img.png'
    
    def get_absolute_url(self):
        pass

class Collection(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        upload_to='categories/%Y/%m/%d', blank=True,
        default='defaults/categories_no_img.png'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'collection'
        verbose_name_plural = 'collections'
    
    def __str__(self):
        return self.name

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return '/media/defaults/categories_no_img.png'

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(
        Collection, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True) 
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)
    stocks = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'), )
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', args=[self.id])
    

    @property
    def get_primary_image(self):
        try:
            return self.images.all()[0]
        except:
            return '/media/defaults/categories_no_img.png'

    def update_stocks(self, quantity):
        quantity = int(quantity)
        if self.stocks < quantity:
            raise ValueError('Not enough stocks')
        self.stocks = self.stocks - quantity
        if(self.stocks == 0):
            self.available = False
        self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.image.url
    