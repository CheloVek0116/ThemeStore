from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Order(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created    = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated    = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    paid       = models.BooleanField(verbose_name='Оплачен', default=False)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ: ' + str(self.id)

    def get_total_cost(self):
        total_cost = sum(item.price for item in self.items.all())
        return total_cost


class OrderItem(models.Model):
    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price   = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)
