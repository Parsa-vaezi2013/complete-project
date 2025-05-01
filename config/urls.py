from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('exchange.urls')),
    path('api/acc/', include('accounts.urls')),
    path('api/accounts/', include('accounts.urls')),
]
