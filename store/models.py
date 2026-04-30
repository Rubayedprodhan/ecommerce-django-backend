from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"







# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='CartItem')
    
#     def __str__(self):
#         return f"Cart of {self.user.username}"
#     @property
#     def total_price(self):
#         total = sum(item.product.price * item.quantity for item in self.items.all())
#         return total
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart of {self.id} for {self.user}"

    @property
    def total_price(self):
      
        total = sum(item.product.price * item.quantity for item in self.items.select_related('product').all())
        return total










class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"  
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity  
    

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"    

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f"Wishlist of {self.user.username}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_status}"
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"
    
class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Inventory for {self.product.name} - {self.quantity} in stock"
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
class ProductSupplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supply_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} supplied by {self.supplier.name}"  
class Return(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for {self.order_item.product.name} - {self.status}"
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
class GiftCard(models.Model):
    code = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Subscription of {self.user.username} to {self.product.name}"
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.read else 'Unread'}"   
class Analytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    purchases = models.IntegerField(default=0)

    def __str__(self):
        return f"Analytics for {self.product.name} - {self.views} views, {self.purchases} purchases"
class Affiliate(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Affiliate {self.user.username} - Code: {self.code}"    
class AffiliateLink(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"Affiliate Link for {self.product.name} by {self.affiliate.user.username}"
    
class ReviewReply(models.Model):
    review = models.ForeignKey(Review, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} to Review {self.review.id}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"
class ProductTag(models.Model):
    product = models.ForeignKey(Product, related_name='tags', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Tag '{self.name}' for {self.product.name}"

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"Attribute '{self.name}' for {self.product.name} - Value: {self.value}"
class ProductReview(models.Model):      
    product = models.ForeignKey(Product, related_name='product_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product Review by {self.user.username} for {self.product.name}"
class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.user.username} for {self.product.name}"
class ProductAnswer(models.Model):
    question = models.ForeignKey(ProductQuestion, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} to Question {self.question.id} for {self.question.product.name}"

class ProductComparison(models.Model):
    product1 = models.ForeignKey(Product, related_name='comparison_product1', on_delete=models.CASCADE)
    product2 = models.ForeignKey(Product, related_name='comparison_product2', on_delete=models.CASCADE)
    comparison_data = models.TextField()

    def __str__(self):
        return f"Comparison between {self.product1.name} and {self.product2.name}"
    
