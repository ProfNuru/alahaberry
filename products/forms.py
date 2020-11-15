from django import forms
from .models import Product,Order,Categorie, Damage


class CreateProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['brand_new','product_name','brand',
				'product_desc','product_details',
				'category','product_price','product_thumbnail',
				'product_image1','product_image2','product_image3',
				'tags']


class CreateProductDamageForm(forms.ModelForm):
	class Meta:
		model = Damage
		fields = ['image','description']


class CreateOrderForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude = ('product','date_ordered','delivered','clerk')
		

class CreateCategoryForm(forms.ModelForm):
	class Meta:
		model = Categorie
		fields = ['category_name','category_image1','category_desc']

