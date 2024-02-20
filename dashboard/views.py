from typing import Any

from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Sum, QuerySet
from dashboard.models import Category

# Create your views here.


class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = (Category.objects.filter(author=self.request.user)
                    .prefetch_related('payments')
                    .annotate(payments_sum=Sum('payments__summa')))
        return queryset
