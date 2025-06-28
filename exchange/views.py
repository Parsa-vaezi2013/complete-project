from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.models import User
from .models import Product, Warehouse
from .serializers import ProductSerializer, WarehouseSerializer
from .utils import get_dollar_price_from_nobitex
from django.core.cache import cache
from decimal import Decimal
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from .models import Product

class ProductListView(ListView, PermissionRequiredMixin):
    model = Product
    permission_required = 'accounts.view_all_products'

    def get(self, request):
        products = Product.objects.all()

        rate = cache.get('usd_to_irr')
        if rate is None:
            rate = get_dollar_price_from_nobitex()
            if rate:
                cache.set('usd_to_irr', rate, timeout=3600)

        for product in products:
            if rate:
                product.price_irr = Decimal(product.price_usd) * Decimal(str(rate))
                product.save()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Product.objects.all(owner=user)
        elif user.role == 'customer':
            return Product.objects.none()


class WarehouseCreateView(APIView):
    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

from rest_framework.generics import ListAPIView
from .models import Product
from .serializers import ProductSerializer

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    def get(self, request):
        return Response({"message": "لطفا از متد POST برای لاگین استفاده کنید."})

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "نام کاربری یا رمز عبور اشتباه است."},
                            status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    
    
    
from rest_framework import permissions

class ProductAccessPermission(permissions.BasePermission):
    """
    - Admin: Full access
    - Seller: Can manage (edit/delete) own products
    - Customer: Can only view products they've visited
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, 'is_seller') and request.user.is_seller

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if hasattr(request.user, 'is_customer') and request.user.is_customer:
            return request.method in permissions.SAFE_METHODS and obj in request.user.visited_products.all()
        
        if hasattr(request.user, 'is_seller') and request.user.is_seller:
            return obj.seller == request.user

        return False


from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product

class UpdateProductPriceView(APIView):
    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'محصول یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        price = request.data.get('price')
        if price is None:
            return Response({'error': 'قیمت وارد نشده'}, status=status.HTTP_400_BAD_REQUEST)

        product.price = price
        product.save()
        return Response({'message': 'قیمت با موفقیت آپدیت شد'}, status=status.HTTP_200_OK)
