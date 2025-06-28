from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# class User(AbstractUser):
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='accounts_user_set',
#         blank=True,
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='accounts_user_permissions_set',
#         blank=True,                                              <--------------این پیشنهاد نشد
#     )

from django.contrib.auth.models import AbstractUser
from django.db import models



from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import Group, Permission


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')


# یا

# class CustomUser(AbstractUser):
#     groups = models.ManyToManyField(
#         Group,
#         related_name='accounts_customuser_groups',
#         blank=True,
#        verbose_name='گروه‌ها'                                        
#     )                                                                 
#     user_permissions = models.ManyToManyField(                       
#         Permission,                                                  
#         related_name='accounts_customuser_permissions',               
#         blank=True,                                                   
#         verbose_name='مجوزهای کاربر'                                
#         )                                  <------------------------- پیشنهاد نشد