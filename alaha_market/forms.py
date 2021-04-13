from django import forms
from products.models import Order, ItemRequest, SoldItem
from customers.models import Subscriber


class CreateOrderForm(forms.ModelForm):
	
	class Meta:
		model = Order
		exclude = ('product','date_ordered','delivered','clerk','delivered_by','cancelled')
		

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]


class RequestForm(forms.ModelForm):
	class Meta:
		model = ItemRequest
		exclude = ('clerk', 'delivered', 'delivered_by', 'date_requested')


class SoldItemForm(forms.ModelForm):
	class Meta:
		model = SoldItem
		fields = ["item", "request", "qty", "amount", "seller_earning"]


