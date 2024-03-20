from django.contrib import admin
from .models import (Category, Product, ProductReview,ProductImage, 
                     Cart, CartProduct, ServeOrder)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(ServeOrder)

