import datetime
from django.db.models import Q
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.

class Contacts(models.Model):
    company_info = HTMLField(verbose_name='Description', max_length=3000, default='')
    extra_info = HTMLField(verbose_name='Extra Info', max_length=1000, default='', null=True, blank=True)

    # department = models.CharField(verbose_name='Department', max_length=30, help_text='Enter Department here')
    # email = models.CharField(verbose_name='Email', max_length=30, help_text='Enter Email here')
    # phone = models.CharField(verbose_name='Phone', max_length=20, help_text='Enter Phone here')

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class ContactsVar(models.Model):
    department = models.CharField(verbose_name='Department', max_length=30, help_text='Enter Department here')
    email = models.CharField(verbose_name='Email', max_length=30, help_text='Enter Email here')
    phone = models.CharField(verbose_name='Phone', max_length=20, help_text='Enter Phone here')
    # other_info = models.ForeignKey(to='Contacts', verbose_name='Inside info', on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    class Meta:
        verbose_name = "Inside"
        verbose_name_plural = "Insides"


class VehicleModel(models.Model):
    model = models.CharField(verbose_name='Model', max_length=20, help_text="Vehicle's model")
    photo = models.ImageField(verbose_name='Photo', upload_to='photos', null=True, blank=True)
    description = HTMLField(verbose_name='Description', max_length=3000, default='')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"


class Status(models.Model):
    name = models.CharField(verbose_name='Status', max_length=50, help_text='Pick your status here', default='Under administration')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Product(models.Model):
    name = models.CharField(verbose_name='Product', max_length=50, help_text='Pick your product here')
    # model = models.ForeignKey(to='VehicleModel', verbose_name='Model', on_delete=models.SET_NULL, null=True, blank=True, related_name='models')
    srvc_photo = models.ImageField(verbose_name='Photo', upload_to='photos', null=True, blank=True)
    srvc_description = HTMLField(verbose_name='Description', max_length=3000, default='')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class ProductPrice(models.Model):
    # name = models.ForeignKey(to='Product', verbose_name='Product', on_delete=models.CASCADE, help_text='Product name for the price')
    price = models.FloatField(verbose_name='Price', help_text='Price for actual product by car model')
    model = models.ForeignKey(to='VehicleModel', verbose_name='Model', on_delete=models.SET_NULL, null=True, blank=True, related_name='models' )
    product = models.ForeignKey(to='Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return f'{self.product} - {self.price} [{self.model}]'


    # def product_price2(self):
    #     return ProductPrice.objects.filter(model=self.model, product=self.product).first().price

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"

#AAA


class Order(models.Model):
    customer = models.ForeignKey(to=User, verbose_name='User', on_delete=models.SET_NULL, null=True, blank=True, help_text='Pick your USER here', )
    date = models.DateTimeField(verbose_name='Date n Time', auto_now_add=True, help_text='Pick your date here', )
    status = models.ForeignKey(to='Status', verbose_name='Status', on_delete=models.SET_NULL, null=True, help_text='Pick your status here', default=6)
    due_back = models.DateField(verbose_name='Will be available', null=True, blank=True, )
    model = models.ForeignKey(to='VehicleModel', verbose_name='Model', on_delete=models.SET_NULL, null=True,
                              blank=True, )




    def order_count(self):
        count = 0
        orders = self.objects.all()
        for order in orders:
            count += order
        return count

    def total(self):
        total = 0
        lines = self.lines.all()
        for line in lines:
            total += line.sum_for()
        return total


    def is_overdue(self):
        return self.due_back and date.today() > self.due_back

    def __str__(self):
        return f'{self.customer} (Model: {self.model}) [{self.date}] - ({self.status} [{self.due_back}])'

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-date']

class OrderLine(models.Model):
    order = models.ForeignKey(to='Order', verbose_name='Order', on_delete=models.CASCADE, help_text='Your orderline here', related_name='lines')
    product = models.ForeignKey(to='Product', verbose_name='Product', on_delete=models.SET_NULL, null=True, help_text='Your product here')
    qty = models.IntegerField(verbose_name='Quantity')


    def __str__(self):
        return f'{self.order.customer} ({self.order.model}): [{self.product}:    x{self.qty}]'

    def product_price(self):
        return ProductPrice.objects.filter(model=self.order.model, product=self.product).first().price

    def sum_for(self):
        return self.product_price() * self.qty


    class Meta:
        verbose_name = "OrderLine"
        verbose_name_plural = "OrderLines"


class OrderComment(models.Model):
    order = models.ForeignKey(to='Order', verbose_name='Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    commentator = models.ForeignKey(to=User, verbose_name='User', on_delete=models.SET_NULL, null=True, blank=True, )
    date_created = models.DateTimeField(verbose_name='Date n Time', auto_now_add=True, )
    comment = models.TextField(verbose_name='Comment', max_length=2000, )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-date_created']


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, verbose_name='User', on_delete=models.CASCADE)
    picture = models.ImageField(verbose_name='Picture', upload_to='profile_pics', default='profile_pics/default.png')


    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

