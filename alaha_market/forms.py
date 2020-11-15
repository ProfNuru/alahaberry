from django import forms
from products.models import Order


class CreateOrderForm(forms.ModelForm):
	
	class Meta:
		model = Order
		exclude = ('product','date_ordered','delivered','clerk','delivered_by','cancelled')
		
