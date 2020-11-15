from django.db import models
from django.urls import reverse
from django.utils import timezone

class SubscriptionPackage(models.Model):
	title = models.CharField(max_length=150)
	cost_per_month = models.DecimalField(decimal_places=2,max_digits=10)
	details = models.TextField(null=True,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('all-packages')

