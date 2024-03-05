from dashboard.models import Category, Payment, Check, Income
from django.contrib import admin

# Register your models here.

admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Check)
admin.site.register(Income)

