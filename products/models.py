from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import string
import random
from django.utils import timezone


# Sample of an ID generator - could be any string/number generator
# For a 6-char field, this one yields 2.1 billion unique IDs
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))


class Categorie(models.Model):
	category_name = models.CharField(max_length=100)
	category_image1 = models.ImageField(null=True, blank=True,default="default.png",upload_to='category_pics')
	category_image2 = models.ImageField(null=True, blank=True,default="default.png",upload_to='category_pics')
	category_desc = models.TextField(null=True, blank=True)
	

	def __str__(self):
		return f'{self.category_name} Category'


	def get_absolute_url(self):
		return reverse('staff-dashboard')


class Product(models.Model):
	product_name = models.CharField(max_length=100)
	product_desc = models.TextField(verbose_name="Product Description",null=True,blank=True)
	product_details = models.TextField(null=True,blank=True)
	product_price = models.DecimalField(verbose_name="Price (GHC)",default=0.00,null=True,blank=True,decimal_places=2,max_digits=10)
	product_thumbnail = models.ImageField(upload_to='product_pics',null=True,blank=True)
	product_image1 = models.ImageField(upload_to='product_pics',null=True,blank=True)
	product_image2 = models.ImageField(upload_to='product_pics',null=True,blank=True)
	product_image3 = models.ImageField(upload_to='product_pics',null=True,blank=True)
	availability = models.BooleanField(default=True)
	brand_new = models.BooleanField(verbose_name="Brand New Item!",default=True)
	featured = models.BooleanField(verbose_name="Discount?",default=False)
	discount_percentage = models.IntegerField(blank=True, null=True, default=0)
	brand = models.CharField(null=True, blank=True,max_length=100)
	quantity = models.IntegerField(blank=True, null=True, default=0)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(null=True, blank=True)
	tags = models.TextField(verbose_name="Hash tags", null=True, blank=True)
	product_uid = models.CharField(blank=True,null=True,max_length=6,unique=True)
	category = models.ForeignKey(Categorie, null=True, blank=True, on_delete=models.CASCADE)
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	negotiable = models.BooleanField(default=False)
	views = models.IntegerField(blank=True, null=True, default=0)
	buy_attempts = models.IntegerField(blank=True, null=True, default=0)
	

	def __str__(self):
		return f'{self.product_name}'


	def get_absolute_url(self):
		return reverse('view-product', kwargs={'pk': self.id, 'productname':self.product_name})


	def save(self, *args, **kwargs):
		if not self.product_uid:
			# Generate ID once, then check the db. If exists, keep trying.
			self.product_uid = id_generator()
			while Product.objects.filter(product_uid=self.product_uid).exists():
				self.product_uid = id_generator()
		super(Product, self).save()


class Damage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(null=False, blank=True, upload_to='product_damages')

	def __str__(self):
		return f'{self.description}'

	def get_absolute_url(self):
		return reverse('add-product-damage', kwargs={'id':self.product.id})


class Order(models.Model):
	clerk = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	product_quantity = models.PositiveIntegerField(default=1)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=15)
	order = models.TextField(null=True, blank=True)
	date_ordered = models.DateTimeField(default=timezone.now)
	delivered = models.BooleanField(default=False)
	cancelled = models.BooleanField(default=False)
	delivered_by = models.TextField(null=True, blank=True)
	recipient = models.CharField(verbose_name="Recipient name (Leave empty if you are the recipient)", null=True,blank=True,max_length=100)
	closest_landmark = models.TextField(verbose_name="Describe the closest landmark to your location",null=True, blank=True)
	delivery_address = models.TextField(verbose_name="Where do you want the item delivered?",blank=True, null=True)
	area = models.CharField(verbose_name="Area",null=True,blank=True,max_length=100)
	house_number = models.CharField(null=True,blank=True,max_length=100)
	

	def __str__(self):
		return f'{self.name} ordered {self.product}'


class ProductHit(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_hit')
	views = models.PositiveIntegerField(default=0)
	effective_hits = models.PositiveIntegerField(default=0)
	last_viewed = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return f'Product:{self.product.product_name}; Views:{self.views}'

