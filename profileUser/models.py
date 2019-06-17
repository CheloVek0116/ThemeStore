from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser):
	avatar      = models.ImageField(blank=True, null=True)
	first_name  = models.CharField(max_length=50, verbose_name='Имя')
	last_name   = models.CharField(max_length=50, verbose_name='Фамилия')

	def __str__(self):
		return self.username

	def get_absolute_url(self):
		return reverse('profileUser:ProfileDetail', kwargs={'username': self.username})

	class Meta:
		verbose_name = 'Прифиль'
		verbose_name_plural = 'Профили'