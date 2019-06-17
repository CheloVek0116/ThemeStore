from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.utils.text import slugify
import os

from django.conf import settings

# Create your models here.


class Category(models.Model):
	name     = models.CharField(max_length=200, verbose_name="Название")

	def get_absolute_url(self):
		pass        

	def __str__(self):
		return self.name



class Product(models.Model):
	author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
	name        = models.CharField(max_length=200, verbose_name="Название")
	slug        = models.SlugField(max_length=200)
	description = models.TextField(blank=True, verbose_name="Описание")
	categories  = models.ManyToManyField('Category', blank=True, verbose_name='Категория', related_name='products')
	price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
	ratings     = GenericRelation(Rating, related_query_name='products')
	created     = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		  return reverse('shop:ProductDetail', kwargs={'username': self.author.username, 'slug': self.slug})

	def save(self, *args, **kwargs):
		self.slug = self.gen_slug(self.name)
		super().save(*args, **kwargs)

	def gen_slug(self, slug):
		slug = slugify(slug, allow_unicode=True)
		return slug

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name + ' by ' + self.author.username

class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	preview = models.BooleanField(default=False)
	image   = models.ImageField()