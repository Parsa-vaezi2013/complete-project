from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from accounts.models import User
from .serializers import RegisterSerializer, LoginSerializer
from exchange.models import Product
from .signals import assign_permissions

class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        print("Content-Type received:", request.content_type)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            if user.objects.filter(username=serializer.validated_data["username"]).exists():
                return Response({"error": "این نام کاربری قبلاً ثبت شده"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "لطفاً برای ثبت‌نام از متد POST استفاده کنید."})


class LoginView(APIView):
    permission_classes = [APIView]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'], 
                password=serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response({"error": "نام کاربری یا رمز عبور اشتباه است"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseProductView(APIView):
    def post(self, request, product_id):
        quantity = request.data.get("quantity", 1)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "تعداد باید عددی مثبت باشد"}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({"error": "تعداد معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "محصول یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
            return Response({"message": "خرید با موفقیت انجام شد"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "موجودی کافی نیست"}, status=status.HTTP_400_BAD_REQUEST)