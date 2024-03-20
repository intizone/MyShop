from main import models
from . import serializers
from .serializers import *
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token


# CATEGORY VIEWS FUNCTIONS

@api_view(['GET'])
def category_list(request):
    categorys = Category.objects.all()
    serializer = CategorySerializer(categorys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    category_serializer = CategorySerializer(category)
    context = {
        'category': category_serializer.data,
    }
    return Response(context)

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def category_update(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def category_delete(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response(status=status.HTTP_200_OK)


# PRODUCT VIEWS FUNCTIONS

@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(quantity__gt=0)  # Only include products with quantity > 0
    serializer = ProductSerializerImage(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def product_update(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def product_delete(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response(status=status.HTTP_200_OK)


# PRODUCT IMAGE VIEWS FUNCTIONS

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def product_image_create(request):
    serializer = ProductImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def product_image_update(request, slug):
    try:
        product_image = ProductImage.objects.get(slug=slug)
    except ProductImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductImageSerializer(product_image, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def product_image_delete(request, slug):
    try:
        product_image = ProductImage.objects.get(slug=slug)
    except ProductImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    product_image.delete()
    return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def add_review(request):
    serializer = ProductReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def cart_list(request):
    active = Cart.objects.filter(is_active=True, user=request.user)
    in_active = Cart.objects.filter(is_active=False, user=request.user).order_by('-id')
    context = {
        'active':CartSerializer(active, many = True).data,
        'in_active':CartSerializer(in_active, many = True).data,
    }
    return Response(context)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def cart_create(request):
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def cart_update(request, slug):
    try:
        cart = Cart.objects.get(slug=slug)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def cart_product_list(request):
    cart_products = CartProduct.objects.all()
    serializer = CartProductSerializer(cart_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def cart_product_create(request):
    serializer = CartProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def cart_product_update(request, slug):
    try:
        cart_product = CartProduct.objects.get(slug=slug)
    except CartProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CartProductSerializer(cart_product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def cart_product_delete(request, slug):
    try:
        cart_product = CartProduct.objects.get(slug=slug)
    except CartProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cart_product.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def serve_order_create(request):
    serializer = ServeOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def sign_in(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user = user)
        info = {
            'token': token.key
        }
    else:
        info = {'fatal':'user not found'}
    return Response(info)


@api_view(['POST'])
def sign_up(request):
    username = request.data['username']
    password = request.data['password']
    confirm_password = request.data['confirm_password']
    if models.User.objects.filter(username = username).first():
        return Response({'fatal':'username already exists'})
    elif password == confirm_password:
        user = models.User.objects.create_user(
            username = username,
            password = password
        )
        user_ser = serializers.UserSerializer(user)
        token, _ = Token.objects.get_or_create(user = user)
        data = {
            'token': token.key,
            'user': user_ser.data
        }
        return Response(data)
    else:
        return Response({'fatal':'check the password you wrote'})



@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def sign_out(request):
    request.user.auth_token.delete()
    return Response({'success' : 'logged out'})





