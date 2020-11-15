from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.urls import reverse
from allauth.account.signals import user_signed_up
from PIL import Image

from subscription_packages.models import SubscriptionPackage
from affiliations.models import Coupon


def user_signed_up_receiver(request, user, **kwargs):
	my_group = Group.objects.get(name='sellers') 
	my_group.user_set.add(user)


user_signed_up.connect(user_signed_up_receiver, sender=User)

class AlahaBerrySetting(models.Model):
	application_name = models.CharField(max_length=150, null=True, blank=True)
	about = models.TextField(null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	contact1 = models.CharField(max_length=20, null=True,blank=True)
	contact2 = models.CharField(max_length=20, null=True, blank=True)
	contact3 = models.CharField(max_length=20, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	google_map = models.TextField(null=True,blank=True)
	region = models.CharField(max_length=20, null=True,blank=True)
	city = models.CharField(max_length=20, null=True,blank=True)
	facebook_url = models.CharField(max_length=250, null=True,blank=True)
	instagram_url = models.CharField(max_length=250, null=True,blank=True)
	twitter_url = models.CharField(max_length=250, null=True,blank=True)
	google_url = models.CharField(max_length=250, null=True,blank=True)
	linkedin_url = models.CharField(max_length=250, null=True,blank=True)
	logo = models.ImageField(default="default.jpg", upload_to='application_images')
	favicon = models.ImageField(verbose_name="Favicon 16X16", default="default.jpg", upload_to='application_images')
	charges_on_sale = models.DecimalField(verbose_name="Percentage charge on sale",default=0.00,null=True,decimal_places=2,max_digits=5)
	commission_on_subscription = models.DecimalField(default=5.00, null=True, decimal_places=3, max_digits=5)
	commission_rate_on_sale = models.DecimalField(verbose_name="Commission rate (%) on sale",default=7.00, null=True, decimal_places=2, max_digits=5)


	def __str__(self):
		return f'{self.application_name} setting'


	def get_absolute_url(self):
		return reverse('staff-dashboard')


class AlahaberryPhoto(models.Model):
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	logo = models.BooleanField(default=False)
	banner = models.BooleanField(default=True)

	def __str__(self):
		return f'Alahaberry photo {self.image.url}'



class Discount(models.Model):
	affiliate_discount = models.IntegerField(verbose_name="Affiliate Discount %",default=25)


	def __str__(self):
		return f'Affiliate discount rate {self.affiliate_discount}%'


	def get_absolute_url(self):
		return reverse('staff-dashboard')


class Subscription(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subscription_package = models.ForeignKey(SubscriptionPackage, on_delete=models.CASCADE, null=True, blank=True)
	total_cost = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
	amount_to_pay = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
	paid = models.BooleanField(default=False)
	months = models.IntegerField(default=0)
	date_subscribed = models.DateTimeField(default=timezone.now)
	subscription_end = models.DateTimeField(default=timezone.now, editable=True)

	def __str__(self):
		return f'{self.user.username} subscribed till {self.user.profile.subscription_end}'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	business_certificate = models.ImageField(blank=True, null=True, upload_to='profile_pics')
	seller_id = models.ImageField(verbose_name="ID", blank=True, null=True, upload_to='profile_pics')
	business_name = models.CharField(max_length=100, default='Alahaberry')
	business_address = models.TextField(max_length=200, default='NA')
	business_description = models.TextField(max_length=250, blank=True, default='NA')
	business_city = models.CharField(max_length=50, blank=True, null=True)
	new_seller = models.BooleanField(default=True, null=True)
	handle_orders = models.BooleanField(default=False)
	phone_number = models.CharField(max_length=100, default='NA')
	date_registered = models.DateTimeField(default=timezone.now)
	subscription_end = models.DateTimeField(default=timezone.now, editable=True)
	affiliated_sales_coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.CASCADE)


	def __str__(self):
		return f'{self.user.username} Profile'


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		try:
			img = Image.open(self.image.path)
			if img.height > 300 or img.width > 300:
				output_size = (300,300)
				img.thumbnail(output_size)
				img.save(self.image.path)
		except:
			print("File not found")


