from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm

from ads.models import Advertisement
from .models import Profile, AlahaBerrySetting



class CustomSignupForm(SignupForm):
	phone = forms.CharField(max_length=12, label='Phone')

	def save(self, request):
		user = super(CustomSignupForm, self).save(request)
		phone_number = self.cleaned_data['phone']
		user.save()
		user.profile.phone_number = phone_number
		user.profile.save()
		return user


class UserRegisterForm(UserCreationForm):
	#email = forms.EmailField()
	phone_number = forms.CharField()

	class Meta:
		#Model to interact with
		model = User

		#Fields to show in form
		fields = ['first_name','last_name','username', 'phone_number', 'password1','password2']



class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		#Model to interact with
		model = User

		#Fields to show in form
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'business_name', 'business_address', 
				'business_city', 'business_certificate', 'seller_id',
				'phone_number','handle_orders']

	def __init__(self, *args, **kwargs):
		check_sales_person = kwargs.pop('check_sales_person', False)
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)
		if check_sales_person:
			del self.fields['business_name'],self.fields['business_address'],self.fields['business_city'],self.fields['business_certificate'],self.fields['handle_orders']



class CreateAdForm(forms.ModelForm):
	class Meta:
		model = Advertisement
		fields = ['title', 'call_to_action','vertical', 'link', 'image','media', 'advertiser','contact']


class AlahaBerrySettingUpdateForm(forms.ModelForm):
	class Meta:
		model = AlahaBerrySetting
		fields = ['application_name','about','logo','favicon','address',
		'contact1','contact2','contact3','email','google_map',
		'region','city','facebook_url','twitter_url','instagram_url',
		'linkedin_url','google_url','charges_on_sale','commission_on_subscription','commission_rate_on_sale']
		
	