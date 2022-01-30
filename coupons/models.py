from django.db import models
import datetime
# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField()
    percentage = models.BooleanField(default=False)
    active = models.BooleanField()

    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        if self.valid_from < datetime.datetime.now() < self.valid_to:
            return True
        return False

    @property
    def is_percentage(self):
        return self.percentage
    
    class Meta:
        verbose_name_plural = 'Coupons'