from django.urls import path
from . import views
urlpatterns = [
   path('products/', views.product_list, name='product-list'),
   path('products/<int:pk>/', views.product_detail, name='product-detail'),
   path('categories/', views.category_list, name='category-list'),
   path('cart/', views.get_cart, name='get-cart'),
   path('cart/add/', views.add_to_cart, name='add-to-cart'),
   path('cart/remove/', views.remove_from_cart, name='remove-from-cart'),
  # path('cart/detail/<int:pk>/', views.cart_detail, name='cart-detail'),
   path('cart/update/', views.update_cart_quantity, name='update-cart-quantity'),

]