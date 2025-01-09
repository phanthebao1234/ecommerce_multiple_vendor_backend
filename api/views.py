from django.db.models import Max
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.serializers import ProductCreateUpdateSerializer, ProductListDetailSerializer, OrderSerializer, ProductInfoSerializer, CategorySerializer, ProductImagesSerializer, FarmerSerializer
from api.models import Product, Order, Category, Farmer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView

class OrderList(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): # Chỉ lấy ra đúng dữ liệu của user đã đăng nhập
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ProductCreateUpdateSerializer
        return ProductListDetailSerializer
    def perform_create(self, serializer): 
        product = serializer.save() 
        images = self.request.FILES.getlist('images') 
        for image in images: 
            ProductImagesSerializer.objects.create(product=product, image=image)
    
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'product_id'
    queryset = Product.objects.all()
    
    def get_permission_classes(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductListDetailSerializer
    
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
class CategoryRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'category_id'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class FarmerListCreateApiView(generics.ListCreateAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    