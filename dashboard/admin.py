from django.contrib import admin

# Register your models here.
from dashboard.models import Category, Payment

admin.site.register(Category)
admin.site.register(Payment)