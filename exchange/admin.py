from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from accounts.models import User
from .models import Product, Warehouse

admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(User)

# admin.site.register(PeriodicTask)
# admin.site.register(IntervalSchedule)