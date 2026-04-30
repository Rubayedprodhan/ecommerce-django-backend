from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, OrderSerializer, UserRegistrationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])

def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, context = {'request': request})
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    
    

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return Response({'message': 'Product added to cart',"cart" :CartSerializer(cart).data})

@api_view(['POST'])
def remove_from_cart(request):
    item_id = request.data.get('item_id')
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return Response({'message': 'Product removed from cart'})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request):
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
    if not item_id or quantity is None:
        return Response({'error': 'Item ID and quantity are required'}, status=400)
    try:
        item = CartItem.objects.get(id=item_id)
        if  quantity < 1:
            item.delete()
            return Response({'message': 'Item removed from cart'})
        item.quantity = quantity
        item.save()
        return Response({'message': 'Cart updated successfully'})
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)       

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_create(request):
    try:
        data = request.data
        name = data.get('name')
        address = data.get('address')
        phone = data.get('phone')
        if not phone.isdigit() or len(phone) < 10:
            return Response({'error': 'Invalid phone number'}, status=400)
        cart, created = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=400)
        total = sum(float(item.product.price) * item.quantity for item in cart.items.all())
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            name=name,
            address=address,
            phone=phone,
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                product=item.product,
                order=order,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()
        return Response({'message': 'Order created successfully', 'order_id': order.id})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
       



# def order_create(request):
#     try:
#        data = request.data
#        name = data.get('name')
#        address = data.get('address')
#        phone = data.get('phone')
#        pyment_method = data.get('payment_method', "COD")
#        cart= Cart.objects.first()
#        if not cart or not cart.items.exists():
#            return Response({'error': 'Cart is empty'}, status=400)
#        total = sum(float(item.product.price) * item.quantity for item in cart.items.all())
#        order = Order.objects.create(
#            user=None,
#            total_amount=total,
#        )

#        for item in cart.items.all():
#            order.items.create(
#                product=item.product,
#                quantity=item.quantity,
#                price=item.product.price
#            )
#        cart.items.all().delete()
#        return Response({'message': 'Order created successfully', 'order_id': order.id})
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)   
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request):  
    serializer = UserRegistrationSerializer(data=request.data)  
    if serializer.is_valid():  
        user = serializer.save()  
        return Response({'message': 'User registered successfully', "user": UserRegistrationSerializer(user)}, status = status.HTTP_201_CREATED)  
    return Response(serializer.errors, status=400)