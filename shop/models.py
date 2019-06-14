from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    avatar      = models.ImageField(blank=True, null=True)
    first_name  = models.CharField(max_length=50, verbose_name='Имя')
    last_name   = models.CharField(max_length=50, verbose_name='Фамилия')
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='Подписчики', related_name='sub')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_page_url', kwargs={'username': self.username})

    class Meta:
        verbose_name = 'Прифиль'
        verbose_name_plural = 'Профили'


class Category(models.Model):
	name     = models.CharField(max_length=200, verbose_name="Название")

	def get_absolute_url(self):
		pass		

	def __str__(self):
		return self.name


class Product(models.Model):
	author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
	name        = models.CharField(max_length=200, db_index=True, verbose_name="Название")
	slug        = models.SlugField(max_length=200, db_index=True)
	description = models.TextField(blank=True, verbose_name="Описание")
	categories  = models.ManyToManyField('Category', blank=True, verbose_name='Категория',related_name='products')
	price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
	ratings     = GenericRelation(Rating, related_query_name='products')
	created     = models.DateTimeField(auto_now_add=True)
	updated     = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		  return reverse('shop:ProductDetail', kwargs={'username': self.author.username, 'slug': self.slug})

	class Meta:
		ordering = ['name']
		index_together = [
			['id', 'slug']
		]

	def __str__(self):
		return self.name + ' by ' + self.author.username


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    preview = models.BooleanField(default=False)
    image = models.ImageField()