import requests

from typing import Any

from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet
from django.views.generic import ListView, View, DetailView

import xml.etree.ElementTree as ET

from dashboard.models import Category, Payment, Check, Income


def get_usd() -> float:
    usd_rate = float(
        ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
        .find('./Valute[CharCode="USD"]/Value')
        .text.replace(',', '.'))
    return usd_rate


def get_eur() -> float:
    eur_rate = float(
        ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
        .find('./Valute[CharCode="EUR"]/Value')
        .text.replace(',', '.'))
    return eur_rate


def get_payment_total_sum(user):
    return Category.objects.filter(author=user).aggregate(payment_total_sum=Sum('payments__summa'))['payment_total_sum']


def get_income_total_sum(user):
    return Category.objects.filter(author=user).aggregate(income_total_sum=Sum('incomes__summa'))['income_total_sum']


def get_payment_history(user):
    return Payment.objects.filter(category__author=user).values('category__name', 'summa', 'data')


def get_income_history(user):
    return Income.objects.filter(category__author=user).values('category__name', 'summa', 'data')


def get_total_income_for_categories(user):
    return (Category.objects.filter(author=user).prefetch_related('incomes').
            annotate(incomes_sum=Sum('incomes__summa')))


class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'categories'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == False:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_anonymous:
            return
        # Общая сумма рассходов
        queryset = (Category.objects.filter(author=self.request.user)
                    .prefetch_related('payments')
                    .annotate(payments_sum=Sum('payments__summa')))
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_anonymous:
            return

        # Общая сумма рассходов
        payment_total_sum = get_payment_total_sum(self.request.user)
        context['payment_total_sum'] = payment_total_sum

        # Общая сумма доходов
        income_total_sum = get_income_total_sum(self.request.user)
        context['income_total_sum'] = income_total_sum

        # История платежей
        payment_history = get_payment_history(self.request.user)
        context['payment_history'] = payment_history

        income_history = get_income_history(self.request.user)
        context['income_history'] = income_history

        #Общая сумма доходов
        total_income_for_categories = get_total_income_for_categories(self.request.user)
        context['total_income_for_categories'] = total_income_for_categories

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

        check = Check.objects.get(id=check_id)
        if check and check.money_in_rub <= int(summa):
            return redirect('home')

        check.money_in_rub -= int(summa)

        if check.currency == 'USD':
            check.money = check.money_in_rub / get_usd()
        elif check.currency == 'EUR':
            check.money = check.money_in_rub / get_eur()
        else:
            check.money -= int(summa)

        check.save()

        payment = Payment(summa=summa, category_id=kwargs.get('pk'), payment_check=check, is_payment=True)
        payment.save()
        return redirect('home')


class IncomeAddView(DetailView):
    model = Category
    template_name = 'income_add.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        checks = Check.objects.filter(author=self.request.user)
        context['checks'] = checks

        return context

    def post(self, request, *args, **kwargs):
        summa = request.POST.get('summa')
        check_id = request.POST.get('radio_check')

        if not check_id:
            return redirect('home')

        check = Check.objects.get(id=check_id)
        if check and check.money_in_rub <= int(summa):
            return redirect('home')

        check.money_in_rub += int(summa)

        if check.currency == 'USD':
            check.money = check.money_in_rub / get_usd()
        elif check.currency == 'EUR':
            check.money = check.money_in_rub / get_eur()
        else:
            check.money += int(summa)

        check.save()

        income = Income(summa=summa, category_id=kwargs.get('pk'), income_check=check, is_payment=True)
        income.save()
        return redirect('home')


class CheckAddView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'check_add.html')

    def post(self, request, *args, **kwargs):
        check_name = request.POST.get('check')
        money = request.POST.get('money')
        currency = request.POST.get('radio_check_currency')

        money_in_rub = 0
        if currency == 'USD':
            money_in_rub = int(money) * get_usd()
        elif currency == 'EUR':
            money_in_rub = int(money) * get_eur()
        else:
            money_in_rub = money

        check = Check(name=check_name, author=request.user, money=int(money),
                      money_in_rub=money_in_rub, currency=currency)
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
        check.save()

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

        if from_check.money >= 0 and from_check.money >= int(summa):
            to_check = Check.objects.get(id=int(check_id))
            if to_check:
                from_check.money -= int(summa)
                to_check.money += int(summa)
                from_check.save()
                to_check.save()

        return redirect('home')

