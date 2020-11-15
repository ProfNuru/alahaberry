from django.db import models
from django.urls import reverse
from django.utils import timezone

class Advertisement(models.Model):
	title = models.CharField(max_length=150)
	call_to_action = models.TextField(verbose_name="Description")
	link = models.CharField(max_length=250)
	image = models.ImageField(null=True,blank=True,upload_to="ad_media")
	media = models.FileField(verbose_name="Short video ad",null=True,blank=True,upload_to="ad_media")
	advertiser = models.CharField(max_length=150)
	contact = models.CharField(max_length=30)
	vertical = models.BooleanField(default=False)
	date_added = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('manage-ads')

