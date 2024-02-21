import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> models.CharField:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Payment(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    summa = models.PositiveIntegerField('Сумма')
    data = models.DateField('Дата', default=datetime.datetime.now)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'