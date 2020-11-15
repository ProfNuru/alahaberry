from django import forms

from .models import Coupon


class AffiliateForm(forms.ModelForm):
	class Meta:
		model = Coupon
		fields = ['coupon_code', 'discount_rate','expiry_date']

