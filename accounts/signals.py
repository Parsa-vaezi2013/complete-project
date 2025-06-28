# from rest_framework.permissions import BasePermission, SAFE_METHODS

# class Is_Staff_User(BasePermission):
#     def has_permission(self, request, view):
#         return bool(
#             request.method in SAFE_METHODS or
#             request.user and 
#             request.is_superuser
#         )
    

# class customer(BasePermission):
#     def has_object_permission(self, request, view, obj):
#          return bool(
#             request.method in SAFE_METHODS or
#             request.user and 
#             request.user == obj.customer.customer
#         )
    
# class seller(BasePermission):
#      def has_object_permission(self, request, view, obj):
#           return bool(
#                request.method in SAFE_METHODS or
#                request.user and
#                request.user == obj.seller.seller
#           )                                          <-----------برای تست


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from .models import User

@receiver(post_save, sender= User)
def assign_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'admin':
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()
        elif instance.role == 'seller':
            perms = Permission.objects.filter(codename__in=[
                'add_product', 'view_all_products', 'view_customer'
            ])
            instance.user_permissions.set(perms)
