from django.db import models
from PIL import Image


class Slide(models.Model):
	slide_image = models.ImageField(null=True, blank=True,upload_to='homepage-slides')
	date_added = models.DateTimeField(auto_now_add=True)
	
