from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

import string
import random
from functools import reduce
from datetime import datetime
from unidecode import unidecode


"""maxsulotlarning qaysi kategoriyada joylashganligi
haqida ma'lumotlar bilan ishlovchi model"""
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify((self.name))
        super(Category, self).save(*args, **kwargs)


"""maxsulotlar haqida ma'lumotlar bilan ishlovchi model"""
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(
        decimal_places=2, 
        max_digits=10, 
        blank=True, 
        null=True
        )
    baner_image = models.ImageField(upload_to='baner/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    @property
    def review(self):
        reviews = ProductReview.objects.filter(product_id=self.id)
        result = reduce(lambda result, x: result +x, reviews, 0)
        try:
            result = result / reviews.count()
        except ZeroDivisionError:
            result = 0
        return result
    
    @property 
    def is_discount(self):
        if self.discount_price is None:
            return 0
        return self.discount_price > 0


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) + '-' + str(self.id) + '-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.slug = self.product.slug
        super(ProductImage, self).save(*args, **kwargs)


"""maxsulotlarga baholarlar qoldirilganligi 
haqida ma'lumotlar bilan ishlovchi model, foydalunuvchi bahosiga qarab
maxsulotning sotuvi oshishi yoki kamayishi mumkin"""
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mark = models.SmallIntegerField()
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}: {self.mark}"

    def save(self, *args, **kwargs):
        self.slug = self.product.slug
        super(ProductReview, self).save(*args, **kwargs)


"""foydalanuvchilar tomonidan sotib olinishga tayyor bo'lgan maxsulotlar
ro'yxatidan tashkil topgan savatchalarni saqlovchi modeldir, 'active'i false 
bo'lsa ushbu cart allaqachon ServerOrder modeliga o'tkazilgan va maxsulotlari sotib olingan"""
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.user.username
        super(Cart, self).save(*args, **kwargs)


    @property
    def quantity(self):
        quantity = 0
        products = CartProduct.objects.filter(product_id = self.id)
        for i in products:
            quantity +=i.quantity
        return quantity

    @property
    def total_price(self):
        result = 0
        for i in CartProduct.objects.filter(card_id=self.id):
            result +=(i.product.price)*i.quantity
        return result


"""har bir savatchadagi har xil maxsulotlarni saqlovchi model"""
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} ta"
    
    def save(self, *args, **kwargs):
        self.slug = self.product.slug + '-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        super(CartProduct, self).save(*args, **kwargs)

    @property
    def total_price(self):
        if self.product.is_discount:
            result = self.product.discount_price * self.quantity
        else:
            result = self.product.price * self.quantity
        return result


"""cartlardagi maxsulotlarni sotib olish uchun rasmiylashtirish 
va yetkazib berish ma'lumotlarini saqlovchi model"""
class ServeOrder(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    phone = models.CharField(max_length=13)
    delivery_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.cart.user.username

    def save(self, *args, **kwargs):
        self.slug = self.cart.user.username
        super(ServeOrder, self).save(*args, **kwargs)
