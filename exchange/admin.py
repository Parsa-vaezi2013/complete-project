from django.contrib import admin

from accounts.models import User
from .models import Product, Warehouse

admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(User)