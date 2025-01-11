import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains') #
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains', 'icontains'], # là phân biệt chữ hoa chữ thường. Nếu bạn cần tìm kiếm không phân biệt chữ hoa chữ thường, hãy sử dụng icontains
            'price' : ['gt', 'lt', 'range'],  # gt: Greater Than(Lớn hơn) | lt: Less Than(nhỏ hơn) | Range
            'category': ['exact'],
        }
        
        # ...path?price__gt=100 | ...path?price__lt=100 | ...path?price__range=15000,20000
        # ** lookup_expr='exact' trong Django filters được sử dụng để chỉ định rằng bộ lọc sẽ thực hiện một phép so khớp chính xác trên trường. 
        # Điều này có nghĩa là giá trị cung cấp phải khớp chính xác với giá trị trường. 
        # Nó tương tự như sử dụng toán tử = trong SQL.