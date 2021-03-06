from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
	email = models.EmailField(unique=True)
	date_subscribed = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.email
