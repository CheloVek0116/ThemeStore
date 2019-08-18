from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

from shop.models import Product


class CartUser(models.Model):
	user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cart')
	products    = models.ManyToManyField(Product, blank=True, verbose_name='продукты', related_name='cart')

	def __str__(self):
		return 'cart of ' + self.user.username

	def get_total_price(self):
		return sum(Decimal(item) for item in self.products.values_list('price', flat=True))

	def clear(self):
		for item in self.products.all():
			self.products.remove(item)

	class Meta:
		verbose_name = 'Корзина'
		verbose_name_plural = 'Корзина'

