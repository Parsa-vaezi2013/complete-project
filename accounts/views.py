from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "این نام کاربری قبلاً ثبت شده"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response({"message": "ثبت‌نام با موفقیت انجام شد"}, status=status.HTTP_201_CREATED)

    def get(self, requests):
        return Response({"message": "Please use POST to register."})

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from exchange.models import CustomUser, Product

class PurchaseProductView(APIView):
    def post(self, request, product_id):
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "محصول یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if product.stock >= int(quantity):
            product.stock -= int(quantity)
            product.save()
            return Response({"message": "خرید با موفقیت انجام شد"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "موجودی کافی نیست"}, status=status.HTTP_400_BAD_REQUEST)

