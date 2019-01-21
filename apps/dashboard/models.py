from django.db import models

from ..LoginAndRegister.models import User
# Create your models here.



class Cart(models.Model):
    product_id=models.CharField(max_length=80)
    brand=models.CharField(max_length=40)
    itemName=models.CharField(max_length=255)
    price=models.FloatField()
    quantity=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user=models.ForeignKey(User,related_name='cart',on_delete=models.DO_NOTHING)

class Order(models.Model):
    order_id=models.CharField(max_length=80)
    brand=models.CharField(max_length=40)
    itemName=models.CharField(max_length=255)
    price=models.FloatField()
    quantity=models.IntegerField()
    totalCost=models.FloatField()
    OrderStatus=models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user=models.ForeignKey(User,related_name='order',on_delete=models.DO_NOTHING)