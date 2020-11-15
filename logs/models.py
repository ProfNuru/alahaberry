from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	log = models.TextField(max_length=200, default='NA')
	date_registered = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f'{self.log}'

