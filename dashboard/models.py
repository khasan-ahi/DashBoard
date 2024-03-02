import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Check(models.Model):
    name = models.CharField('Название', max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    money = models.IntegerField('Сумма')

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
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
