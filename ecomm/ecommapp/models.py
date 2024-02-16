from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    price=models.PositiveBigIntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='image',null=True)
    description=models.CharField(max_length=100)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    options=(
        ('in-cart','in-cart'),
        ('cancelled','cancelled'),
        ('order-placed','order-placed'),
    )
    status=models.CharField(max_length=100,choices=options,default='in-cart')


class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True)
    address=models.TextField(max_length=255)
    email=models.EmailField()
    options=(
        ('order-placed','order-placed'),
        ('cancelled','cancelled'),
        ('dispatched','dispatched'),
        ('delivered','delivered')

    )
    status=models.CharField(max_length=100,choices=options,default='order-placed')