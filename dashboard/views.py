from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView
from django.db.models import Sum, QuerySet

from dashboard.models import Category, Payment


# Create your views here.


class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_anonymous:
            return
        queryset = (Category.objects.filter(author=self.request.user)
                    .prefetch_related('payments')
                    .annotate(payments_sum=Sum('payments__summa')))
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.user.is_anonymous:
            return
        context = super().get_context_data(**kwargs)
        total_sum = Category.objects.filter(
            author=self.request.user).aggregate(total_sum=Sum('payments__summa'))['total_sum']

        payment_history = Payment.objects.filter(category__author=self.request.user).values('category__name', 'summa', 'data')
        context['payment_history'] = payment_history

        context['total_sum'] = total_sum
        return context


class CategoryAddView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'category_add.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('category')
        category = Category(name=name, author=request.user)
        category.save()
        return redirect('home')


class PaymentAddView(DetailView):
    model = Category
    template_name = 'payment_add.html'

    def post(self, request, *args, **kwargs):
        summa = request.POST.get('summa')
        payment = Payment(summa=summa, category_id=kwargs.get('pk'))
        payment.save()
        return redirect('home')
