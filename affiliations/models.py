from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Coupon(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	coupon_code = models.CharField(max_length=100, default='NA')
	sponsorship = models.BooleanField(default=False)
	discount_rate = models.IntegerField(default=0)
	date_added = models.DateTimeField(default=timezone.now)
	expiry_date = models.DateTimeField(default=timezone.now, editable=True)


	def __str__(self):
		return f'Coupon code: {self.coupon_code}'


class Commission(models.Model):
	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	commission = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
	commission_instance = models.CharField(null=True, default="Subscription", max_length=24)
	paid = models.BooleanField(default=False)
	date_used = models.DateTimeField(default=timezone.now)
	subscriber = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


	def __str__(self):
		return f'Commission: {self.coupon}'

