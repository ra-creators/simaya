
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField( max_length=200)
    discription=models.TextField()
    blog_img=models.ImageField(upload_to='blogimg')

