
from django.db import models
from accounts.models import CustomUser

class Warehouse(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    price_irr = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    seller = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True, blank=True)



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


