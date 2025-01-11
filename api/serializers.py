from rest_framework import serializers
from .models import Product, User, Order, OrderItem, Category, Farmer, Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title', 'slug', 'imageUrl', 'description', 'createdAt', 'updatedAt')

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','images')

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    farmer = serializers.PrimaryKeyRelatedField(queryset=Farmer.objects.all())
    class Meta: 
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'category',
            'farmer',
            'createdAt',
            'updatedAt'
        )
        
        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError("Price must be greater than 0")
            return value
        
        def validate_stock(self, value):
            if value == 0:
                raise serializers.ValidationError("Product is out of stock")
            return value
        
class ProductListDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer() 
    farmer = FarmerSerializer()
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'category',
            'farmer',
            'createdAt',
            'updatedAt'
        )
        
        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError("Price must be greater than 0")
            return value
        
        def validate_stock(self, value):
            if value == 0:
                raise serializers.ValidationError("Product is out of stock")
            return value
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = 'product.name' )
    product_price = serializers.DecimalField(source = 'product.price', max_digits =10, decimal_places =2)

    class Meta:
        model = OrderItem
        fields = ('quantity', 'product_name', 'product_price', 'item_subtotal')

        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # items ở đây phải đúng với items trong related_name của OrderItem trong model ( Nested serializers)
    # nếu không sử dụng mối quan hệ lồng nhau như trên thì khi response thì items sẽ trả về các id đại diện cho bản OrderItem đó
    
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    
    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    def get_total_quantity(self, obj):
        order_items = obj.items.all()
        return sum(order_item.quantity for order_item in order_items)
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created',
            'user',
            'status',
            'total_price',
            'items',
            'total_quantity'
        )
        
class ProductInfoSerializer(serializers.Serializer):
    # get product, max_price, count
    products = ProductListDetailSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)