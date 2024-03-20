from django.urls import path
from . import views

# token = 'fd6ef961fba10f1336dcc4eb4737fa983c1eedbe'

urlpatterns = [
    # category
    path('category_list/', views.category_list, name='category-list'),
    path('category/<str:slug>/', views.category_detail, name='category-detail'),
    path('category_create/', views.category_create, name='category-create'),
    path('category_update/<str:slug>/', views.category_update, name='category-update'),
    path('category_delete/<str:slug>/', views.category_delete, name='category-delete'),

    # product
    path('product_list/', views.product_list, name='product-list'),
    path('product_create/', views.product_create, name='product-create'),
    path('product_update/<str:slug>/', views.product_update, name='product-update'),
    path('product_delete/<str:slug>/', views.product_delete, name='product-delete'),
    path('add_review/', views.add_review, name='add-review'),

    # product image
    path('product_image_create/', views.product_image_create, name='product-image-create'),
    path('product_image_update/<str:slug>/', views.product_image_update, name='product-image-update'),
    path('product_image_delete/<str:slug>/', views.product_image_delete, name='product-image-delete'),

    # cart
    path('cart_list/', views.cart_list, name='cart-list'),
    path('cart_create/', views.cart_create, name='cart-create'),
    path('cart_update/<str:slug>/', views.cart_update, name='cart-update'),

    # cart product
    path('cart_product_list/', views.cart_product_list, name='cart-product-list'),
    path('cart_product_create/', views.cart_product_create, name='cart-product-create'),
    path('cart_product_update/<str:slug>/', views.cart_product_update, name='cart-product-update'),
    path('cart_product_delete/<str:slug>/', views.cart_product_delete, name='cart-product-delete'),
    
    # oder
    path('order_create/', views.serve_order_create, name='order-create'),

    # auth
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),
    ]