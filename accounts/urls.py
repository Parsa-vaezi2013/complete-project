from django.urls import path
from .views import PurchaseProductView, RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/<int:product_id>/purchase/', PurchaseProductView.as_view(), name='purchase-product'),
    path("register/", RegisterView.as_view(), name="register"),
]


