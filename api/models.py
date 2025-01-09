import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
    
class User(AbstractUser):
    pass

class Coupon(models.Model):
    title = models.CharField(max_length=200)
    couponCode = models.CharField(max_length=255)
    expiryDate = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Post(models.Model):
    slug = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.post.title
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    imageUrl = models.CharField(max_length=200)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Farmer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    code = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    physicalAddress = models.CharField(max_length=200)
    contactPerson = models.CharField(max_length=200)
    contactPersonPhone = models.IntegerField()
    term = models.TextField()
    notes = models.TextField()
    isActive = models.BooleanField(default=True)
    image = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.id}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category_name')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True, related_name='farmer_name')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
class ProductImage(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images') 
    image = models.ImageField(upload_to='products/') 
    
    def __str__(self): 
        return f"Image for {self.product.name}"
    
class Market(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)  
    
class Order(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'
        
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    
    product = models.ManyToManyField(Product, through="OrderItem", related_name="orders")
    
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') # phải trùng với items ở trong serializers 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"