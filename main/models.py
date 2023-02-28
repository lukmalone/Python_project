from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Category name', max_length=200, help_text='Enter category')
    description = models.TextField('Description', max_length=2000, default='')

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    price = models.FloatField()
    in_stock = models.BooleanField(default=True)
    quantity = models.IntegerField('Quantity', help_text='Item quantity', null=False)
    cover = models.ImageField('Cover', upload_to='covers', null=True)

    class Meta:
        verbose_name_plural = 'Products'
        # ordering = ('-created_at',)

    def __str__(self):
        return self.title

class Order(models.Model):
    title = models.CharField('Title', help_text='Title of the service', max_length=50, null=False)
    date = models.DateField('Date', help_text='Order\'s date', null=False)
    ordered_item = models.ForeignKey('Product', on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField('Quantity', help_text='Item quantity', null=False)
    price = models.FloatField('Price', help_text='Order price')

    def __str__(self):
        return f'{self.ordered_item}x{self.quantity}({self.price})'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True)
    # image = models.ImageField(upload_to='images/', default='images/default.png')

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)
    
    # class Meta:
    #     verbose_name = "Review"
    #     verbose_name_plural = 'Reviews'
    #     ordering = ['-date_created']

    def __str__(self):
        return f'{self.product.title}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"