from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView
from django.db.models import Sum, QuerySet

from dashboard.models import Category, Payment, Check


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
        context['total_sum'] = total_sum

        payment_history = Payment.objects.filter(category__author=self.request.user).values('category__name', 'summa', 'data')
        context['payment_history'] = payment_history

        checks = Check.objects.filter(author=self.request.user)
        context['checks'] = checks

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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        checks = Check.objects.filter(author=self.request.user)
        context['checks'] = checks

        return context

    def post(self, request, *args, **kwargs):
        summa = request.POST.get('summa')
        check_id = request.POST.get('radio_check')
        is_on = request.POST.get('is_payment')

        is_payment = False
        if is_on:
            is_payment = True

        check = Check.objects.get(id=check_id)
        if check.money <= int(summa):
            return redirect('home')

        if is_payment:
            check.money -= int(summa)
        else:
            check.money += int(summa)
        check.save()

        payment = Payment(summa=summa, category_id=kwargs.get('pk'), payment_check=check, is_payment=is_payment)
        payment.save()
        return redirect('home')


class CheckAddView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'check_add.html')

    def post(self, request, *args, **kwargs):
        check_name = request.POST.get('check')
        money = request.POST.get('money')
        check = Check(name=check_name, author=request.user, money=int(money))
        check.save()
        return redirect('home')


class CheckDeleteView(DetailView):
    model = Check
    template_name = 'check_delete.html'

    def post(self, requsest, *args, **kwargs):
        check = Check.objects.get(id=kwargs.get('pk'))
        check.delete()
        return redirect('home')


class CheckUpdateView (DetailView):
    model = Check
    template_name = 'check_update.html'

    def post(self, request, *args, **kwargs):
        check_name = request.POST.get('check')
        money = request.POST.get('money')
        check = Check.objects.filter(id=kwargs.get('pk')).update(name=check_name, money=money)

        return redirect('home')


class CheckTransferView(DetailView):
    model = Check
    template_name = 'check_transfer.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        checks = Check.objects.filter(author=self.request.user)
        context['checks'] = checks

        return context

    def post(self, request, *args, **kwargs):
        summa = request.POST.get('summa')
        check_id = request.POST.get('radio_check')

        from_check = Check.objects.filter(id=kwargs.get('pk')).get()
        print(from_check.name, 'asd')

        if from_check.money >= 0 and from_check.money >= int(summa):
            to_check = Check.objects.get(id=int(check_id))
            if to_check:
                from_check.money -= int(summa)
                to_check.money += int(summa)
                from_check.save()
                to_check.save()

        return redirect('home')

