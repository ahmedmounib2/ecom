from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)

    # dont pluralize address
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    

# create order Model
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length= 15000)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order- {str(self.id)}'



# create order items Model

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null= True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null= True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'