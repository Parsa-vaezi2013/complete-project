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

class ProductListView(APIView):
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