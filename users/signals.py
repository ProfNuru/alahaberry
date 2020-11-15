from django.db.models.signals import (post_save, pre_delete)
from django.contrib.auth.signals import (user_logged_in, 
										user_logged_out, 
										user_login_failed)
from django.contrib.auth.models import User,Group
from django.dispatch import receiver
from products.models import Product,ProductHit
from affiliations.models import Coupon

from .models import Profile

#Send signal when User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


#Catch user creation signal and save user profile
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()


#Send signal when User is created
@receiver(post_save, sender=Product)
def create_producthit(sender, instance, created, **kwargs):
	if created:
		ProductHit.objects.create(product=instance)


#Catch user creation signal and save user profile
@receiver(post_save, sender=Product)
def save_producthit(sender, instance, **kwargs):
	instance.product_hit.save()




#Send signal when User is created
@receiver(post_save, sender=User)
def create_coupon(sender, instance, created, **kwargs):
	if created:
		Coupon.objects.create(user=instance, coupon_code=instance.username)


#Catch user creation signal and save user profile
@receiver(post_save, sender=User)
def save_coupon(sender, instance, **kwargs):
	group = Group.objects.get(name='affiliates')
	if group in instance.groups.all():
		instance.coupon.save()

