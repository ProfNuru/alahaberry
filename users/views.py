from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.utils import timezone
from django.core import serializers

import datetime
import pytz
import decimal
from dateutil.relativedelta import relativedelta
import json

from products.models import Product, ProductHit, Order, Categorie, ItemRequest, SoldItem
from products.forms import CreateProductForm
from logs.models import Log
from ads.models import Advertisement
from subscription_packages.models import SubscriptionPackage
from affiliations.models import Coupon, Commission

from .decorators import unauthenticated_user, staff_only, allowed_users
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CreateAdForm
from .models import Profile, Subscription, AlahaBerrySetting, Discount


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			
			#Assign new user to group
			group = Group.objects.get(name='sellers')
			user.groups.add(group)
			user.save()

			if request.user.is_authenticated and request.user.groups.filter(name__in=['admins']).exists():
				messages.success(request, f'New Seller {username} added!')
				return redirect('manage-users')
			messages.success(request, f'Account for {username} created successfully!')
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', {'form':form})


@login_required
@staff_only
def staff_dashboard(request):
	if request.user.groups.filter(name='affiliates').exists():
		return redirect('sales-person')
	context = {
		'categories': Categorie.objects.all(),
		'products': Product.objects.all(),
		'sellers': User.objects.filter(groups__name='sellers'),
		'orders': Order.objects.all(),
		'delivered_orders': Order.objects.filter(delivered=True),
		'today': timezone.now(),
	}
	return render(request, 'users/staff_dashboard.html',context)


@login_required
@staff_only
def all_orders(request):
	context = {
		'orders': ItemRequest.objects.all(),
		'pending_orders': ItemRequest.objects.filter(delivered=False),
		'delivered_orders': ItemRequest.objects.filter(delivered=True)
	}
	return render(request, 'users/all_orders.html', context)


@login_required
def get_order_details(request):
	if request.is_ajax():
		order_id = int(request.GET['order_id'].strip())
		curr_order = ItemRequest.objects.get(id=order_id)
		sell_rate = AlahaBerrySetting.objects.last()
		items_list = []
		ordered_items = SoldItem.objects.select_related('item','request').filter(request__id=order_id)
		for item in ordered_items:
			items_list.append({
				'product_id':item.item.id,
				'product_uid':item.item.product_uid,
				'product_name':item.item.product_name,
				'qty_ordered':item.qty,
				'amount':float(item.amount),
				'sell_cost':'{:.2f}'.format(float(item.seller_earning)),
				'seller':item.item.seller.username,
				'seller_id':item.item.seller.id
			})

		items_dict = {
			'items_list':items_list,
			'delivered':curr_order.delivered,
			'customer_email':curr_order.customer_email,
			'customer_phone':curr_order.customer_phone
		}
		json_items = json.dumps(items_dict)
		return JsonResponse(json_items, safe=False, status=200)
	return redirect('all-orders')


@login_required
def make_delivery(request):
	if request.is_ajax():
		order_id = int(request.GET['order_id'].strip())
		order = ItemRequest.objects.get(id=order_id)
		order.delivered = True
		order.save()
		return JsonResponse(json.dumps({'delivered':True}), safe=False, status=200)
	return redirect('all-orders')


@login_required
def deliver_order(request):
	if request.method == 'POST':
		app_settings = AlahaBerrySetting.objects.first()
		orderId = request.POST['order_id']
		order_to_deliver = Order.objects.get(id=orderId)
		order_to_deliver.clerk = request.user
		order_to_deliver.delivered = True
		if order_to_deliver.product.seller.groups.filter(name__in=['affiliates']).exists():
			print("Sale by sales person")
			total_amt = order_to_deliver.product_quantity * order_to_deliver.product.product_price
			commission = total_amt * (app_settings.commission_rate_on_sale/100)
			new_commission = Commission(coupon=order_to_deliver.product.seller.coupon,
							commission=commission,subscriber=order_to_deliver.product.seller)
			new_commission.save()
		order_to_deliver.save()

		messages.success(request, f'Order for {order_to_deliver.product.product_uid} delivered to {order_to_deliver.name}!')
	return redirect('all-orders')



@login_required
@staff_only
def all_subscriptions(request):
	if request.method == 'POST':
		current_datetime = datetime.datetime.now(tz=pytz.UTC)
		sub_request_id = request.POST['subscription_request_id']
		subscribe = Subscription.objects.get(id=sub_request_id, paid=False)
		months = subscribe.months
		sub_delta = relativedelta(months=months)

		if subscribe.user.profile.subscription_end <= current_datetime:
			subscribe.subscription_end = current_datetime + sub_delta
		else:
			subscribe.subscription_end = subscribe.user.profile.subscription_end + sub_delta

		subscribe.date_subscribed = current_datetime
		subscribe.paid = True
		subscribe.user.profile.subscription_end = subscribe.subscription_end
		
		#Record commission
		if subscribe.user.profile.affiliated_sales_coupon:
			app_settings = AlahaBerrySetting.objects.first()
			coupon = subscribe.user.profile.affiliated_sales_coupon
			commission = app_settings.commission_on_subscription
			subscriber = subscribe.user

			new_commission = Commission(coupon=coupon,commission=commission,subscriber=subscriber)
			new_commission.save()

		subscribe.user.save()
		subscribe.save()

		messages.success(request, f'Subscription granted!')
		return redirect('all-subscriptions')

	context = {
		'subscriptions': Subscription.objects.all(),
		'subscription_requests': Subscription.objects.filter(paid=False),
	}
	return render(request, 'users/all_subscriptions.html', context)


@login_required
@allowed_users(allowed_roles=['sellers','affiliates'])
def user_dashboard(request):
	current_datetime = datetime.datetime.now(tz=pytz.UTC)
	subbed = False
	affiliated = False
	if request.user.profile.subscription_end > current_datetime or request.user.groups.filter(name__in=['affiliates']).exists():
		subbed = True

	if request.user.coupon.expiry_date > current_datetime:
		affiliated = True

	pdts = Product.objects.filter(seller=request.user)
	item_hits = 0
	for p in pdts:
		item_hits += p.product_hit.views

	context = {
		'subscriptions': Subscription.objects.filter(user=request.user),
		'products': pdts,
		'subbed': subbed,
		'item_hits':item_hits,
		'affiliated': affiliated,
		'orders': Order.objects.filter(product__seller=request.user, delivered=False)
	}
	return render(request,'users/user_dashboard.html',context)


@login_required
@allowed_users(allowed_roles=['sellers'])
def subscriptions(request):
	shop_documents_uploaded = False

	if request.user.profile.business_certificate or request.user.profile.seller_id:
		shop_documents_uploaded = True

	if request.method == 'POST':
		app_settings = AlahaBerrySetting.objects.first()
		commission = app_settings.commission_on_subscription
		package_id = request.POST['package_id']
		package = SubscriptionPackage.objects.get(id=int(package_id))
		months = request.POST['sub_months']
		total_cost = package.cost_per_month * int(months)
		amount_to_pay = total_cost

		if not request.user.profile.new_seller and request.user.profile.affiliated_sales_coupon:
			coupon = request.user.profile.affiliated_sales_coupon

			if not coupon.user.groups.filter(name__in=['affiliates']).exists():
				messages.warning(request, f'Invalid Coupon code!')
			elif coupon.discount_rate <= 0:
				discount_rate = decimal.Decimal(Discount.objects.first().affiliate_discount/100)
				discount_amt = total_cost * discount_rate
				amount_to_pay = total_cost - discount_amt
			else:
				discount_rate = decimal.Decimal(coupon.discount_rate/100)
				discount_amt = total_cost * discount_rate
				amount_to_pay = total_cost - discount_amt

		elif bool(request.POST['coupon_code']) and Coupon.objects.filter(coupon_code=request.POST['coupon_code']).exists():
			coupon_code = request.POST['coupon_code']
			coupon = Coupon.objects.get(coupon_code=coupon_code)
			
			if not coupon.user.groups.filter(name__in=['affiliates']).exists():
				messages.warning(request, f'Invalid Coupon code!')
			elif coupon.discount_rate <= 0:
				discount_rate = decimal.Decimal(Discount.objects.first().affiliate_discount/100)
				discount_amt = total_cost * discount_rate
				amount_to_pay = total_cost - discount_amt
			else:
				discount_rate = decimal.Decimal(coupon.discount_rate/100)
				discount_amt = total_cost * discount_rate
				amount_to_pay = total_cost - discount_amt

			request.user.profile.affiliated_sales_coupon = coupon
			request.user.profile.save()

		elif not Coupon.objects.filter(coupon_code=request.POST['coupon_code']).exists():
			messages.warning(request, f'Invalid Coupon code!')

		else:
			discount = 0
			amount_to_pay = total_cost - (total_cost * discount)
		
		###### To payment Gateway #######
		# current_datetime = datetime.datetime.now(tz=pytz.UTC)
		# sub_delta = relativedelta(months=int(months))
		# if request.user.profile.subscription_end <= current_datetime:
		# 	subscription_end = current_datetime + sub_delta
		# 	new_Subscription = Subscription(user=request.user, 
		# 			subscription_package=package,
		# 			months=int(months), total_cost=total_cost, 
		# 			amount_to_pay=amount_to_pay, paid=True,subscription_end=subscription_end)
		# 	new_Subscription.save()
		# 	request.user.profile.subscription_end = subscription_end
		# 	request.user.profile.save()
		# else:
		# 	subscription_end = request.user.profile.subscription_end + sub_delta
		# 	new_Subscription = Subscription(user=request.user, 
		# 			subscription_package=package, 
		# 			months=int(months), total_cost=total_cost, 
		# 			amount_to_pay=amount_to_pay, paid=True,subscription_end=subscription_end)
		# 	new_Subscription.save()
		# 	request.user.profile.subscription_end = subscription_end
		# 	request.user.profile.save()
		new_Subscription = Subscription(user=request.user, 
							subscription_package=package,
							months=int(months), total_cost=total_cost, 
							amount_to_pay=amount_to_pay)
		new_Subscription.save()

		#Log commission
		# new_commission = Commission(coupon=request.user.profile.affiliated_sales_coupon,commission=commission,subscriber=request.user)
		# new_commission.save()

		if request.user.profile.new_seller:
			request.user.profile.new_seller = False
			request.user.profile.save()

		return redirect('subscriptions')


	current_datetime = datetime.datetime.now(tz=pytz.UTC)
	subbed = False
	affiliated = False
	if request.user.profile.subscription_end > current_datetime:
		subbed = True

	if request.user.coupon.expiry_date > current_datetime:
		affiliated = True

	context = {
		'subscriptions': Subscription.objects.filter(user=request.user),
		'subscription_packages': SubscriptionPackage.objects.all(),
		'subbed': subbed,
		'affiliated': affiliated,
		'shop_documents_uploaded': shop_documents_uploaded
	}
	return render(request, 'users/subscriptions.html', context)


@login_required
@allowed_users(allowed_roles=['admins'])
def manage_users(request):
	current_datetime = datetime.datetime.now(tz=pytz.UTC)
	sellers = User.objects.filter(groups__name='sellers')
	context = {
		'sellers': sellers,
		'subbed_sellers': Profile.objects.filter(subscription_end__gt=current_datetime,user__groups__name='sellers'),
		'expired_sellers': Profile.objects.filter(subscription_end__lte=current_datetime,user__groups__name='sellers'),
		'add_seller_form': UserRegisterForm()
	}
	return render(request, 'users/manage_users.html',context)


@login_required
@allowed_users(allowed_roles=['admins'])
def item_sales(request):
	sales = SoldItem.objects.all()
	total_sales_amt = 0
	total_paid_amt = 0
	total_unpaid_amt = 0
	for sale in sales:
		total_sales_amt += sale.amount
		if sale.payment_made:
			total_paid_amt += sale.seller_earning
		else:
			total_unpaid_amt += sale.seller_earning

	context = {
		'total_sales_amt':total_sales_amt,
		'total_paid_amt':total_paid_amt,
		'total_unpaid_amt':total_unpaid_amt,
		'sales': sales
	}
	return render(request, 'users/item_sales.html',context)


@login_required
@allowed_users(allowed_roles=['admins','sellers'])
def individual_sales(request):
	sales = SoldItem.objects.filter(item__seller=request.user)
	total_sales_amt = 0
	total_paid_amt = 0
	total_unpaid_amt = 0
	for sale in sales:
		total_sales_amt += sale.amount
		if sale.payment_made:
			total_paid_amt += sale.seller_earning
		else:
			total_unpaid_amt += sale.seller_earning

	context = {
		'total_sales_amt':total_sales_amt,
		'total_paid_amt':total_paid_amt,
		'total_unpaid_amt':total_unpaid_amt,
		'sales': sales
	}
	return render(request, 'users/individual_sales.html',context)



@login_required
@allowed_users(allowed_roles=['admins'])
def make_payment_to_seller(request,s_id):
	sale = SoldItem.objects.get(id=s_id)
	sale.payment_made = True
	sale.save()
	return redirect('item-sales')

@login_required
@allowed_users(allowed_roles=['admins'])
def manage_clerks(request):
	clerks = User.objects.filter(groups__name='clerks')
	context = {
		'clerks': clerks,
		'add_clerk_form': UserRegisterForm()
	}
	return render(request, 'users/all_clerks.html',context)



@login_required
@allowed_users(allowed_roles=['admins'])
def activity_log(request):
	context = {
		'logs': Log.objects.all(),
		'latest_logs': Log.objects.filter(date_registered__gt=timezone.now()-relativedelta(days=1))
	}
	return render(request, 'users/activity_log.html', context)


@login_required
def profile(request):
	check_sales_person = False
	if request.user.groups.filter(name__in=['affiliates','clerks']).exists():
		check_sales_person = True

	current_datetime = datetime.datetime.now(tz=pytz.UTC)
	subbed = False

	if request.user.profile.subscription_end > current_datetime:
		subbed = True

	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile,
									check_sales_person=check_sales_person)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()

			messages.success(request, f'Account Updated!')
			return redirect('profile-page')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	
	context = {
		'u_form': u_form,
		'p_form': p_form,
		'subbed': subbed
	}


	return render(request, 'users/user_profile.html', context)


@login_required
@allowed_users(allowed_roles=['admins','clerks'])
def seller_profile(request,name):
	seller = User.objects.get(username=name)
	context = {
		'seller': seller
	}

	return render(request, 'users/seller_profile.html', context)


@login_required
@allowed_users(allowed_roles=['admins'])
def admin_add_clerk(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			phone = form.cleaned_data.get('phone_number')
			
			#Assign new user to group
			group = Group.objects.get(name='clerks')
			user.groups.add(group)
	
			messages.success(request, f'New Clerk {username} added!')
			return redirect('manage-clerks')
	else:
		messages.error(request, f'Failed to add clerk!')
		return redirect('manage-clerks')


@login_required
@staff_only
def admin_view_ad(request, id):
	ad = Advertisement.objects.get(id=id)

	context = {
		'ad': ad
	}
	return render(request, 'users/admin_ad_view.html',context)


@login_required
@staff_only
def admin_edit_item(request, id):
	item = Product.objects.get(id=id)
	if request.method == 'POST':
		form = CreateProductForm(request.POST,request.FILES,instance=item)
		if form.is_valid():
			form.save()

			messages.success(request, f'Item {item.product_name} editted successfully!')
			return redirect('staff-dashboard')
		else:
			return render(request, 'users/admin_edit_item.html', {'form':form})

	
	form = CreateProductForm(instance=item)
	return render(request, 'users/admin_edit_item.html', {'form':form})
	

@login_required
@allowed_users(allowed_roles=['admins'])
def admin_delete_item(request, id):
	product = Product.objects.get(id=id)
	context = {'item':product}
	if request.method == 'POST':
		item_name = product.product_name
		product.delete()
		messages.success(request, f'Item {item_name} deleted successfully!')
		return redirect('staff-dashboard')

	return render(request, 'users/admin_delete_item.html', context)
	


@allowed_users(allowed_roles=['admins'])
def manage_ads(request):
	if request.method == "POST":
		ad_form = CreateAdForm(request.POST,request.FILES)
		print(request.FILES)
		if ad_form.is_valid():
			ad_form.save()
			messages.success(request, f'Ad added!')
			return redirect('manage-ads')

	ad_form = CreateAdForm(request.POST,request.FILES)
	ads = Advertisement.objects.all()

	context = {
		'ads': ads,
		'ad_form': ad_form
	}

	return render(request, 'users/manage_ads.html', context)


class UpdateAdView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Advertisement
	template_name = 'users/ad_form.html'
	fields = ['title','call_to_action',
	'link','image','media',
	'advertiser','contact','vertical']
	success_message = "Ad editted!"


	def test_func(self):
		group = self.request.user.groups.all()[0].name
		if group in ['admins','clerks']:
			return True
		return False


class DeleteAdView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
	model = Advertisement
	template_name = 'users/ad_confirm_delete.html'
	context_object_name = 'ad'
	success_url = '/staff_dashboard/manage_ads/'
	success_message = "Ad deleted!"


	def test_func(self):
		group = self.request.user.groups.all()[0].name
		if group in ['admins','clerks']:
			return True
		return False
	

class AlahaBerrySettingUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = AlahaBerrySetting
	template_name = 'users/general_settings.html'
	fields = ['application_name','about','logo','cover_photo','favicon',
			'address','contact1','contact2','contact3','email',
			'google_map','region','city','facebook_url','twitter_url',
			'instagram_url','linkedin_url','google_url','charges_on_sale',
			'commission_on_subscription','commission_rate_on_sale']
	success_message = "General Settings updated!"

	def test_func(self):
		product = self.get_object()
		if self.request.user.groups.all()[0].name == 'admins':
			return True
		return False



class DiscountSettingUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Discount
	template_name = 'users/discount_settings.html'
	fields = ['affiliate_discount']
	success_message = "Discount Settings updated!"

	def test_func(self):
		product = self.get_object()
		if self.request.user.groups.all()[0].name == 'admins':
			return True
		return False



