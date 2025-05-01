from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    price_irr = models.BigIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    def decrease_stock(self, amount=1):
        if self.quantity >= amount:
            self.quantity -= amount
            self.save(update_fields=['quantity'])
            return True
        return False



# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',  # تغییر در اینجا
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_permissions_set',  # تغییر در اینجا
        blank=True,
    )
