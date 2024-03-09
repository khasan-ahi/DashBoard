import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


# Модель счета
class Check(models.Model):
    name = models.CharField('Название', max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    money = models.IntegerField('Сумма')
    money_in_rub = models.IntegerField('Сумма в рублях', default=0)

    class Currency(models.TextChoices):
        USD = 'USD', _('USD')
        EUR = 'EUR', _('EUR')
        RUB = 'RUB', _('RUB')

    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.RUB)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счеты'


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Модель рассходов
class Payment(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True
    )
    payment_check = models.ForeignKey(
        'Check',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True
    )

    summa = models.PositiveIntegerField('Сумма')
    is_payment = models.BooleanField(default=True)
    data = models.DateField('Дата', default=datetime.datetime.now)

    def __str__(self) -> str:
        return str(self.summa)

    class Meta:
        verbose_name = 'Рассход'
        verbose_name_plural = 'Рассходы'


# Модель доходов
class Income(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='incomes',
        null=True
    )
    income_check = models.ForeignKey(
        'Check',
        on_delete=models.CASCADE,
        related_name='incomes',
        null=True
    )

    summa = models.PositiveIntegerField('Сумма')
    is_payment = models.BooleanField(default=True)
    data = models.DateField('Дата', default=datetime.datetime.now)

    def __str__(self) -> str:
        return str(self.summa)

    class Meta:
        verbose_name = 'Доход'
        verbose_name_plural = 'Доходы'
