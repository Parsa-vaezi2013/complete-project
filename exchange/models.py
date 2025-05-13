
from django.db import models
from accounts.models import CustomUser
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
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def decrease_stock(self, amount=1):
        if self.quantity >= amount:
            self.quantity -= amount
            self.save(update_fields=['quantity'])
            return True
        return False





from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='exchange_customuser_groups',
        blank=True,
        verbose_name='گروه‌ها'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='exchange_customuser_permissions',
        blank=True,
        verbose_name='مجوزهای کاربر'
    )



