from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category, Cart, CartItem
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
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
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=None)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=None)
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
    