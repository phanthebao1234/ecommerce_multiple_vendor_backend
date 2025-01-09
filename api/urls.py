from django.urls import path
from .import views

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('categories/', views.CategoryListCreateAPIView.as_view()),
    path('categories/<int:category_id>/', views.CategoryRetriveUpdateDestroyAPIView.as_view()),
    path('orders/', views.OrderList.as_view()),
    path('product/info/', views.ProductInfoAPIView.as_view()),
    path('farmers/', views.FarmerListCreateApiView.as_view()),
]
