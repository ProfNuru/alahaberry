from django import forms

from .models import SubscriptionPackage


class SubscriptionPackageForm(forms.ModelForm):
	class Meta:
		model = SubscriptionPackage
		fields = ['title', 'cost_per_month','details']

