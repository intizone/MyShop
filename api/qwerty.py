



@api_view(["GET"])
def cart_detail(request, slug ):
    cart = models.Cart.objects.get(slug =slug )
    items = models.CartProduct.objects.filter(card=cart)
    context = {
        'cart':serializers.CartSerializer(cart),
        'items':serializers.CartProductSerializer(items, many = True)
    }
    return Response(context)


@api_view(["GET, POST"])
@login_required(login_url='main:login')
def create_cart(request, slug):           #agar foydalanuvchida Cart bo'lmasa yoki u aktiv bo'lmasa yangi Cart yaratadi
    product = models.Product.objects.get(slug = slug)
    cart = models.Cart.objects.filter(user = request.user, is_active = True).first()
    if cart:
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    else:
        new_cart = models.Cart.objects.create(
            user = request.user
        )
        serializer = serializers.CartSerializer(new_cart)
        return Response(serializer.data)

@api_view(["GET, POST"])
def add_to_cart(request, id_product, id_user):
    product = models.Product.objects.get(id = id_product)
    cart = models.Cart.objects.get(user_id = id_user, is_active = True)
    previous_url = request.META.get('HTTP_REFERER')
    if models.CartProduct.objects.filter(product_id = id_product, card = cart).first():
        data = models.CartProduct.objects.get(product_id = id_product, card = cart)
        data.quantity +=1
        data.save()
        serializer = serializers.CartProductSerializer(data)
        return Response (serializer.data)
    else:
        data = models.CartProduct.objects.create(
            product = product,
            card = cart,
            )
        serializer = serializers.CartProductSerializer(data)
        return Response (serializer.data)




@api_view(['POST, GET'])
def order_cart(request, slug):
    cart = models.Cart.objects.get(slug=slug)
    objects = models.CartProduct.objects.filter(card = cart)
    for obj in objects:
        prod = models.Product.objects.get(id = obj.product.id)
        new_quant = obj.product.quantity-obj.quantity

        if new_quant>=0:
            prod.quantity = new_quant
            prod.save()
            data = models.Overall.objects.get(product = obj.product)
            data.all_outcome +=obj.quantity
            data.save()
            models.ProductOut.objects.create(
                product = prod,
                amount = obj.quantity
            )
        else:
            obj.quantity = prod.quantity
            prod.quantity = 0
            obj.save()
            prod.save()
            data = models.Overall.objects.get(product = obj.product)
            data.all_outcome += obj.quantity
            data.save()
            models.ProductOut.objects.create(
                product = prod,
                amount = obj.quantity
            )

    cart.is_active = False
    cart.save()
    return Response ({'detail':'ordered succesfully'})

@api_view(['GET'])
def cart_detail_delete(request):
    try:
        item_id = request.GET['items_id']
        item = models.CartProduct.objects.get(id=item_id)
        item.delete()
        return Response({'detail': 'Cart item deleted successfully'})
    except models.CartProduct.DoesNotExist:
        return Response({'error': 'Cart item not found'})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reviewing(request, slug):

    """ bu funksiyada review yaratilmagan bo'lsa yaratadi, mavjud bo'lsa update qiladi. Review_CREATE, review_UPDATE"""

    data = models.ProductReview.objects.filter(product__slug = slug, user = request.user).first()
    if not data:
        if request.method == "POST":
            new = models.ProductReview.objects.create(
                user = request.user,
                product = models.Product.objects.get(id =id),
                mark = request.data.get('mark')
            )
            serializer = serializers.ProductReviewSerializer(new)
            context = {
                'report': 'created succesfully',
                'new_review' : serializer.data
            }
            return Response(context)
        else:
            return Response({'report': 'not POSTed yet',
                             'status': 'creation'})
    else:
        if request.method == 'POST':
            data.mark = request.data.get('mark')
            data.save()
            serializer = serializers.ProductReview(data)
            context = {
                'report': 'updated succesfully',
                'updated_review': serializer
            }
            return Response(context)
        
        else:
            return Response({'report': 'not POSTed yet',
                             'status': 'Updating session'})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_active(request):
    data = models.Cart.objects.filter(user = request.user, is_active = True).first()
    
    if data:
        serializer = serializers.CartSerializer(data)
        return Response(serializer.data)
    else:
        return Response({"report": 'you do not have any active cart yet'})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_inactive(request):
    data = models.Cart.objects.filter(user = request.user, is_active = False)
    if data.first():
        serializer = serializers.CartSerializer(data, many = True)
        return Response(serializer.data)
    else:
        return Response({"report": 'you do not have any inactive cart yet'})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_update(request, slug):
    data = models.Cart.objects.filter(slug=slug)
    if data.first():
        cart = data.first()
        objects = models.CartProduct.objects.filter(card = cart)
        for obj in objects:
            prod = models.Product.objects.get(id = obj.product.id)
            new_quant = obj.product.quantity-obj.quantity

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_product_delete(request,slug): # id -> product_id
    cart = models.Cart.objects.filter(user = request.user, is_active = True).first()
    if cart:
        expect = models.CartProduct.objects.filter(card__is_active = True, product__slug = slug).first()
        print(expect)
        if expect:
            if expect.quantity > 1:
                expect.quantity-=1
                expect.save()
                serializer = serializers.CartProductSerializer(expect)
                return Response ({"detail": "Your cart-product's quantity reduced by one", "cart_product" : serializer.data})
            elif expect.quantity == 1:
                expect.delete()
                return Response ({'detail': 'cart-product deleted successfully'})

        else:
            return Response ({'detail': 'you do not have that cart_product to delete'})

    else:
        ({'detail': 'you do not have cart and cart_product to delete'})
