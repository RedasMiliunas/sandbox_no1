from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class VehicleModel(models.Model):
    model = models.CharField(verbose_name='Model', max_length=20, help_text="Vehicle's model")

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"


class Status(models.Model):
    name = models.CharField(verbose_name='Status', max_length=50, help_text='Pick your status here')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Product(models.Model):
    name = models.CharField(verbose_name='Product', max_length=50, help_text='Pick your product here')
    model = models.ForeignKey(to='VehicleModel', verbose_name='Model', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class ProductPrice(models.Model):
    name = models.ForeignKey(to='Product', verbose_name='Product', on_delete=models.CASCADE, help_text='Product name for the price')
    price = models.FloatField(verbose_name='Price', help_text='Price for actual product by car model')
    model = models.ForeignKey(to='VehicleModel', verbose_name='Model', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.price} [{self.model}]'

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"

#AAA


class Order(models.Model):
    customer = models.ForeignKey(to=User, verbose_name='User', on_delete=models.CASCADE, help_text='Pick your USER here')
    date = models.DateTimeField(verbose_name='Date n Time', auto_now_add=True, help_text='Pick your date here')
    status = models.ForeignKey(to='Status', verbose_name='Status', on_delete=models.SET_NULL, null=True, help_text='Pick your status here')

    def __str__(self):
        return f'{self.customer}: [{self.date} - {self.status}]'

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderLine(models.Model):
    order = models.ForeignKey(to='Order', verbose_name='Order', on_delete=models.CASCADE, help_text='Your orderline here')
    product = models.ForeignKey(to='Product', verbose_name='Product', on_delete=models.SET_NULL, null=True , help_text='Your product here')
    qty = models.IntegerField(verbose_name='Quantity')

    def __str__(self):
        return f'{self.order}: [{self.product} x {self.qty}]'


    class Meta:
        verbose_name = "OrderLine"
        verbose_name_plural = "OrderLines"