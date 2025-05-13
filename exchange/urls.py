from itertools import product
from django.urls import path
from .views import LoginView, WarehouseCreateView, ProductListView, SignupView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('warehouses/', WarehouseCreateView.as_view(), name='warehouses'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
]


from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls
